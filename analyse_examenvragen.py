#!/usr/bin/env python3
"""
Script om examenvragen uit PDF's te analyseren en in te delen volgens
de HAVO Biologie syllabus domeinen.

Havo Biologie syllabus domeinen (2024):
1. Inleiding
2. Voeding en vertering
3. Stofwisseling van de cel
4. Bloedsomloop
5. Ademhaling
6. Uitscheiding
7. Zenuwstelsel en hormonen
8. Waarnemen
9. Beweging
10. Afweer
11. Erfelijkheid
12. Evolutie
13. Ecologie
14. Gedrag
15. Plantenfysiologie
"""

import re
from collections import defaultdict

# Havo Biologie syllabus domeinen
DOMEINEN = {
    "Voeding en vertering": [
        r"voeding|vertering|spijsvertering|enzym|amylase|pepsine|lipase|gal|alvleesklier|speeksel|maag|darm|darmen|vill(i|us)|resorptie|koolhydraat|eiwit|vet|voedingsstof|voedingsstoffen|glucose|glycogeen|zetmeel|cellulose"
    ],
    "Stofwisseling van de cel": [
        r"stofwisseling|celademhaling|glycolyse|krebscyclus|elektronentransportketen|ATP|ADP|NAD|FAD|mitochondri(um|ën)|chloroplast|fotosynthese|glucose|zuurstof|kooldioxide|energie|aerobe|anaerobe|melkzuur|gisting"
    ],
    "Bloedsomloop": [
        r"bloed|bloedsomloop|hart|slagader|ader|haarvat|capillair|bloedvat|bloedvaten|bloeddruk|bloedplasma|rode bloedcellen|witte bloedcellen|bloedplaatjes|hemoglobine|zuurstoftransport|kooldioxidetransport|hartslag|puls|bloedgroep"
    ],
    "Ademhaling": [
        r"ademhaling|long|longen|alveol(i|en)|luchtpijp|bronchi(us|ën)|diafragma|borstholte|inademen|uitademen|zuurstof|O2|kooldioxide|CO2|gaswisseling|ademhalingscentrum|ademfrequentie|ademvolume"
    ],
    "Uitscheiding": [
        r"uitscheiding|nier|nieren|nefron|urine|blaas|ureum|ammoniak|zure stofwisseling|lever|gal|ontgiftiging|transpiratie|zweten|huid"
    ],
    "Zenuwstelsel en hormonen": [
        r"zenuwstelsel|hersenen|ruggenmerg|zenuw|zenuwen|neuron|synaps|neurotransmitter|hormoon|hormonen|endocrien|hypofyse|bijnier|schildklier|alvleesklier|insuline|glucagon|adrenaline|testosteron|oestrogeen|progesteron|groei|homeostase|reflex|prikkel|reactie"
    ],
    "Waarnemen": [
        r"waarnemen|oog|netvlies|hoornvlies|lens|glasvocht|staafje|kegeltje|kleur|accommodatie|gehoor|oor|trommelvlies|gehoorbeentjes|slakkenhuis|gehoorzenuw|reuk|smaak|tast|evenwicht"
    ],
    "Beweging": [
        r"beweging|spier|spieren|skelet|bot|beenderen|gewricht|pees|bewegingsstelsel|spiercontractie|actine|myosine|ATP|bewegingspatroon|reflexboog"
    ],
    "Afweer": [
        r"afweer|immuunsysteem|witte bloedcellen|lymfocyt|antistof|antigeen|vaccin|vaccinatie|infectie|ziekteverwekker|bacterie|bacteriën|virus|virussen|ontsteking|koorts|allergie|auto-immuun|HIV|AIDS"
    ],
    "Erfelijkheid": [
        r"erfelijkheid|gen|genen|DNA|chromosoom|chromosomen|allel|allelen|homozygoot|heterozygoot|dominant|recessief|overerving|Mendel|kruising|stamboom|mutatie|genmutatie|genetische variatie|genetica|PCR|DNA-sequencing|epigenetica"
    ],
    "Evolutie": [
        r"evolutie|natuurlijke selectie|Darwin|soortvorming|speciatie|adaptatie|aanpassing|variatie|selectiedruk|fitness|overleving|fortplanting|evolutiebiologie|fylogenie|homonogie|analogie|convergentie|divergentie|fossiel|fossielen|mutatie|genetische drift|genenstroom"
    ],
    "Ecologie": [
        r"ecologie|ecosysteem|populatie|gemeenschap|biotoop|abiotisch|biotisch|voedselketen|voedselweb|producent|consument|reductor|trofisch niveau|energiestroom|koolstofkringloop|stikstofkringloop|waterkringloop|symbiose|parasitisme|mutualisme|commensalisme|concurrentie|niche|habitat|biodiversiteit|milieu|vervuiling|klimaatverandering"
    ],
    "Gedrag": [
        r"gedrag|ethologie|instinct|aangeleerd|conditionering|klassieke conditionering|operante conditionering|beloning|straf|imprinting|sociaal gedrag|groepsgedrag|hiërarchie|territorialiteit|communicatie|signaal|feromoon|agressie|vluchtgedrag|voortplantingsgedrag|broedzorg"
    ],
    "Plantenfysiologie": [
        r"plant|planten|fotosynthese|chlorofyl|bladeren|blad|stengel|wortel|xyleem|floëem|houtvat|zeefvat|transpiratie|osmose|turgor|groei|hormoon|auxine|gibberelline|cytokinine|ethyleen|abscisinezuur|bloei|bestuiving|bevruchting|zaad|kieming|plantenveredeling"
    ]
}


def extract_text_from_pdf_content(text):
    """Extract text from PDF content by finding text between [( and )] TJ"""
    matches = re.findall(r'\[(.*?)\] TJ', text)
    
    all_text = []
    for match in matches:
        # Remove PDF escape sequences like \001y
        clean = re.sub(r'\[\\x[0-9a-fA-F]{2}\]', '', match)
        clean = re.sub(r'\([a-zA-Z0-9]+\)', '', clean)
        clean = re.sub(r'[\x00-\x1F\x7F-\xFF]', '', clean)
        clean = re.sub(r'\s+', ' ', clean).strip()
        if clean and len(clean) > 2:
            all_text.append(clean)
    
    return ' '.join(all_text)


def clean_text(text):
    """Further clean extracted text"""
    # Remove remaining PDF artifacts
    text = re.sub(r'\([a-zA-Z]+\)', '', text)  # Remove things like \001y
    text = re.sub(r'[\x00-\x1F\x7F-\xFF]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[\x80-\xFF]', '', text)  # Remove extended ASCII
    return text.strip()


def identify_questions(text):
    """Identify questions in the text"""
    # Patterns that indicate a question
    question_patterns = [
        r'\b(Noteer|Schrijf|Beschrijf|Leg uit|Verklaar|Geef|Noem|Welke|Wat|Hoe|Waarom|Waar|Wanneer|Wie|Hoeveel|Hoe lang)\b',
        r'\b(Is|Zijn|Heeft|Hebben|Kun|Kan|Wordt|Worden|Geldt|Gelden)\b.*\?',
        r'\b(juist|onjuist|waar|niet waar|correct|fout)\b',
        r'\b(1p|2p|3p|4p|5p|\d+\s*punt)\b',
        r'\b(vraag|opgave|onderdeel)\b.*\d+',
    ]
    
    questions = []
    for pattern in question_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            # Extract context around the match
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 200)
            context = text[start:end].strip()
            if context not in questions:
                questions.append(context)
    
    return questions


def categorize_by_domain(text, questions):
    """Categorize text and questions by syllabus domain"""
    domain_matches = defaultdict(list)
    
    # Check each domain
    for domain, patterns in DOMEINEN.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                domain_matches[domain].append(pattern)
    
    # For questions, try to categorize each
    question_domains = defaultdict(list)
    for q in questions:
        for domain, patterns in DOMEINEN.items():
            for pattern in patterns:
                if re.search(pattern, q, re.IGNORECASE):
                    question_domains[domain].append(q)
                    break  # Only assign to first matching domain
            else:
                question_domains["Onbekend"].append(q)
    
    return domain_matches, question_domains


def main():
    pdf_files = ['2025I.txt', '2025I bijlage.txt', '2025II.txt']
    
    all_results = {}
    
    for pdf_file in pdf_files:
        print(f"\n{'='*60}")
        print(f"Analyseren: {pdf_file}")
        print('='*60)
        
        try:
            with open(pdf_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract text
            extracted = extract_text_from_pdf_content(content)
            clean = clean_text(extracted)
            
            print(f"\nExtracted {len(clean)} characters of clean text")
            
            # Identify questions
            questions = identify_questions(clean)
            print(f"Found {len(questions)} potential questions")
            
            # Categorize
            domain_matches, question_domains = categorize_by_domain(clean, questions)
            
            # Print domain matches
            print("\n--- Domeinen gevonden in tekst ---")
            for domain, patterns in domain_matches.items():
                print(f"  {domain}: {len(patterns)} matches")
            
            # Print questions by domain
            print("\n--- Vragen per domein ---")
            for domain, qs in question_domains.items():
                if qs:
                    print(f"\n{domain} ({len(qs)} vragen):")
                    for i, q in enumerate(qs[:5], 1):  # Show first 5 per domain
                        print(f"  {i}. {q[:150]}...")
                    if len(qs) > 5:
                        print(f"  ... en {len(qs) - 5} meer")
            
            # Save results
            all_results[pdf_file] = {
                'text_length': len(clean),
                'questions': questions,
                'domain_matches': domain_matches,
                'question_domains': question_domains
            }
            
        except FileNotFoundError:
            print(f"ERROR: File {pdf_file} not found")
        except Exception as e:
            print(f"ERROR: {e}")
    
    # Generate summary
    print("\n" + "="*60)
    print("SAMENVATTING")
    print("="*60)
    
    total_questions = 0
    domain_counts = defaultdict(int)
    
    for pdf_file, results in all_results.items():
        print(f"\n{pdf_file}:")
        print(f"  Totaal: {results['text_length']} karakters")
        print(f"  Vragen: {len(results['questions'])}")
        total_questions += len(results['questions'])
        
        for domain, qs in results['question_domains'].items():
            if domain != "Onbekend":
                domain_counts[domain] += len(qs)
    
    print("\n" + "="*60)
    print("VERDELING VRAAG PER DOMEIN (totaal)")
    print("="*60)
    
    for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_questions) * 100 if total_questions > 0 else 0
        print(f"{domain:30s}: {count:3d} ({percentage:5.1f}%)")
    
    if total_questions > 0:
        unknown_count = total_questions - sum(domain_counts.values())
        if unknown_count > 0:
            percentage = (unknown_count / total_questions) * 100
            print(f"{'Onbekend':30s}: {unknown_count:3d} ({percentage:5.1f}%)")
    
    print(f"\nTotaal aantal vragen: {total_questions}")


if __name__ == '__main__':
    main()
