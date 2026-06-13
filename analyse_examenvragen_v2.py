#!/usr/bin/env python3
"""
Verbeterd script om examenvragen uit PDF's te analyseren en in te delen
volgens de HAVO Biologie syllabus domeinen.
"""

import re
from collections import defaultdict

# Havo Biologie syllabus domeinen
DOMEINEN = {
    "Voeding en vertering": [
        r"voeding|vertering|spijsvertering|enzym|amylase|pepsine|lipase|gal|alvleesklier|speeksel|maag|darm|darmen|villi|resorptie|koolhydraat|eiwit|vet|voedingsstof|voedingsstoffen|glucose|glycogeen|zetmeel|cellulose"
    ],
    "Stofwisseling van de cel": [
        r"stofwisseling|celademhaling|glycolyse|krebscyclus|elektronentransport|ATP|ADP|NAD|FAD|mitochondri|chloroplast|fotosynthese|glucose|zuurstof|kooldioxide|energie|aerobe|anaerobe|melkzuur|gisting"
    ],
    "Bloedsomloop": [
        r"bloed|bloedsomloop|hart|slagader|ader|haarvat|capillair|bloedvat|bloeddruk|bloedplasma|rode bloedcel|witte bloedcel|bloedplaatje|hemoglobine|zuurstoftransport|kooldioxidetransport|hartslag|puls|bloedgroep"
    ],
    "Ademhaling": [
        r"ademhaling|long|longen|alveoli|alveolus|luchtpijp|bronchus|bronchi|diafragma|borstholte|inademen|uitademen|zuurstof|O2|kooldioxide|CO2|gaswisseling|ademhalingscentrum|ademfrequentie|ademvolume"
    ],
    "Uitscheiding": [
        r"uitscheiding|nier|nieren|nefron|urine|blaas|ureum|ammoniak|zure stofwisseling|lever|gal|ontgiftiging|transpiratie|zweten|huid"
    ],
    "Zenuwstelsel en hormonen": [
        r"zenuwstelsel|hersenen|ruggenmerg|zenuw|neuron|synaps|neurotransmitter|hormoon|hormonen|endocrien|hypofyse|bijnier|schildklier|alvleesklier|insuline|glucagon|adrenaline|testosteron|oestrogeen|progesteron|groei|homeostase|reflex|prikkel|reactie"
    ],
    "Waarnemen": [
        r"waarnemen|oog|netvlies|hoornvlies|lens|glasvocht|staafje|kegeltje|kleur|accommodatie|gehoor|oor|trommelvlies|gehoorbeentje|slakkenhuis|gehoorzenuw|reuk|smaak|tast|evenwicht"
    ],
    "Beweging": [
        r"beweging|spier|spieren|skelet|bot|beenderen|gewricht|pees|bewegingsstelsel|spiercontractie|actine|myosine|ATP|bewegingspatroon|reflexboog"
    ],
    "Afweer": [
        r"afweer|immuunsysteem|witte bloedcel|lymfocyt|antistof|antigeen|vaccin|vaccinatie|infectie|ziekteverwekker|bacterie|virus|ontsteking|koorts|allergie|auto-immuun|HIV|AIDS|milt|lymfe"
    ],
    "Erfelijkheid": [
        r"erfelijkheid|gen|genen|DNA|chromosoom|chromosomen|allel|allelen|homozygoot|heterozygoot|dominant|recessief|overerving|Mendel|kruising|stamboom|mutatie|genmutatie|genetische variatie|genetica|PCR"
    ],
    "Evolutie": [
        r"evolutie|natuurlijke selectie|Darwin|soortvorming|speciatie|adaptatie|aanpassing|variatie|selectiedruk|fitness|overleving|fortplanting|evolutiebiologie|fylogenie|fossiel|fossielen|genetische drift|genenstroom"
    ],
    "Ecologie": [
        r"ecologie|ecosysteem|populatie|gemeenschap|biotoop|abiotisch|biotisch|voedselketen|voedselweb|producent|consument|reductor|trofisch|energiestroom|koolstofkringloop|stikstofkringloop|waterkringloop|symbiose|parasitisme|mutualisme|commensalisme|concurrentie|niche|habitat|biodiversiteit|milieu|vervuiling|klimaat"
    ],
    "Gedrag": [
        r"gedrag|ethologie|instinct|aangeleerd|conditionering|klassieke conditionering|operante conditionering|beloning|straf|imprinting|sociaal gedrag|groepsgedrag|hiërarchie|territorialiteit|communicatie|signaal|feromoon|agressie|vluchtgedrag|voortplantingsgedrag|broedzorg"
    ],
    "Plantenfysiologie": [
        r"plant|planten|fotosynthese|chlorofyl|blad|bladeren|stengel|wortel|xyleem|floëem|houtvat|zeefvat|transpiratie|osmose|turgor|groei|hormoon|auxine|gibberelline|cytokinine|ethyleen|bloei|bestuiving|bevruchting|zaad|kieming"
    ]
}


def clean_pdf_text(text):
    """Extract and clean text from PDF content"""
    # Extract all text between [( and )]
    matches = re.findall(r'\[(.*?)\]', text)
    
    cleaned_parts = []
    for match in matches:
        # Remove PDF escape sequences
        part = re.sub(r'\[\\x[0-9a-fA-F]{2}\]', '', match)
        part = re.sub(r'\([a-zA-Z0-9]+\)', '', part)
        part = re.sub(r'[\x00-\x1F\x7F-\xFF]', '', part)
        part = re.sub(r'\s+', ' ', part).strip()
        if part and len(part) > 2:
            cleaned_parts.append(part)
    
    # Join and do final cleaning
    full_text = ' '.join(cleaned_parts)
    
    # Remove remaining artifacts
    full_text = re.sub(r'[()\-]+', ' ', full_text)
    full_text = re.sub(r'\s+', ' ', full_text)
    full_text = re.sub(r'[\x00-\x1F\x7F-\xFF]', '', full_text)
    full_text = re.sub(r'\d+\.\d+', '', full_text)  # Remove numbers like 1.5, 2.3
    full_text = re.sub(r'\d+p', '', full_text)  # Remove like "2p"
    full_text = re.sub(r'\d+', '', full_text)  # Remove standalone numbers
    
    return full_text.strip()


def identify_questions(text):
    """Identify questions in the text based on keywords"""
    # Split into sentences
    sentences = re.split(r'[.!?]', text)
    
    question_keywords = [
        'Noteer', 'Schrijf', 'Beschrijf', 'Leg uit', 'Verklaar', 'Geef',
        'Noem', 'Welke', 'Wat', 'Hoe', 'Waarom', 'Waar', 'Wanneer', 'Wie',
        'Hoeveel', 'Hoe lang', 'Is', 'Zijn', 'Heeft', 'Hebben', 'Kun',
        'Kan', 'Wordt', 'Worden', 'Geldt', 'Gelden', 'juist', 'onjuist',
        'waar', 'niet waar', 'correct', 'fout', 'onderdeel', 'vraag',
        'opgave', 'punt', 'p', 'Licht toe', 'Verklaar waarom'
    ]
    
    questions = []
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # Check if sentence contains a question keyword
        for keyword in question_keywords:
            if keyword.lower() in sentence.lower():
                # Clean up the question
                q = re.sub(r'\s+', ' ', sentence)
                q = q.strip()
                if q and len(q) > 10:
                    questions.append(q)
                break
    
    return questions


def categorize_question(question, domains=DOMEINEN):
    """Categorize a single question by domain"""
    for domain, patterns in domains.items():
        for pattern in patterns:
            if re.search(pattern, question, re.IGNORECASE):
                return domain
    return "Onbekend"


def categorize_all(text, questions):
    """Categorize all questions by domain"""
    domain_questions = defaultdict(list)
    
    for q in questions:
        domain = categorize_question(q)
        domain_questions[domain].append(q)
    
    # Also check which domains appear in the full text
    domain_in_text = set()
    for domain, patterns in DOMEINEN.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                domain_in_text.add(domain)
                break
    
    return domain_questions, domain_in_text


def main():
    pdf_files = ['2025I.txt', '2025I bijlage.txt', '2025II.txt']
    
    all_results = {}
    
    for pdf_file in pdf_files:
        print(f"\n{'='*70}")
        print(f"Analyseren: {pdf_file}")
        print('='*70)
        
        try:
            with open(pdf_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Clean text
            clean_text = clean_pdf_text(content)
            print(f"\nGereinigde tekst: {len(clean_text)} karakters")
            
            # Identify questions
            questions = identify_questions(clean_text)
            print(f"Gevonden vragen: {len(questions)}")
            
            # Categorize
            domain_questions, domain_in_text = categorize_all(clean_text, questions)
            
            # Print domains found in text
            print("\n--- Domeinen gevonden in tekst ---")
            for domain in sorted(domain_in_text):
                print(f"  ✓ {domain}")
            
            # Print questions by domain
            print("\n--- Vragen per domein ---")
            for domain in sorted(domain_questions.keys()):
                qs = domain_questions[domain]
                if qs:
                    print(f"\n{domain} ({len(qs)} vragen):")
                    for i, q in enumerate(qs[:3], 1):
                        # Truncate long questions
                        display_q = q[:120] + "..." if len(q) > 120 else q
                        print(f"  {i}. {display_q}")
                    if len(qs) > 3:
                        print(f"     ... en {len(qs) - 3} meer")
            
            # Save results
            all_results[pdf_file] = {
                'text_length': len(clean_text),
                'questions': questions,
                'domain_questions': domain_questions,
                'domain_in_text': domain_in_text
            }
            
        except FileNotFoundError:
            print(f"ERROR: File {pdf_file} not found")
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    # Generate summary
    print("\n" + "="*70)
    print("SAMENVATTING")
    print("="*70)
    
    total_questions = 0
    domain_counts = defaultdict(int)
    
    for pdf_file, results in all_results.items():
        print(f"\n{pdf_file}:")
        print(f"  Tekst: {results['text_length']} karakters")
        print(f"  Vragen: {len(results['questions'])}")
        total_questions += len(results['questions'])
        
        for domain, qs in results['domain_questions'].items():
            if domain != "Onbekend":
                domain_counts[domain] += len(qs)
    
    print("\n" + "="*70)
    print("VERDELING VRAAG PER DOMEIN (totaal)")
    print("="*70)
    
    # Sort by count
    sorted_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)
    
    for domain, count in sorted_domains:
        percentage = (count / total_questions) * 100 if total_questions > 0 else 0
        print(f"{domain:30s}: {count:3d} ({percentage:5.1f}%)")
    
    if total_questions > 0:
        unknown_count = total_questions - sum(domain_counts.values())
        if unknown_count > 0:
            percentage = (unknown_count / total_questions) * 100
            print(f"{'Onbekend':30s}: {unknown_count:3d} ({percentage:5.1f}%)")
    
    print(f"\nTotaal aantal vragen: {total_questions}")
    
    # Print all domains found
    all_domains_found = set()
    for results in all_results.values():
        all_domains_found.update(results['domain_in_text'])
    
    print("\n" + "="*70)
    print("ALLE DOMEINEN DIE IN TEKST VOORKOMEN")
    print("="*70)
    for domain in sorted(all_domains_found):
        print(f"  ✓ {domain}")


if __name__ == '__main__':
    main()
