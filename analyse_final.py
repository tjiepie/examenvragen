#!/usr/bin/env python3
"""
Final script voor analyse van examenvragen volgens HAVO Biologie syllabus domeinen.
"""

import re
from collections import defaultdict

# HAVO Biologie syllabus domeinen
DOMEINEN = {
    "Voeding en vertering": [
        r"voeding|vertering|spijsvertering|enzym|amylase|pepsine|lipase|gal|alvleesklier|speeksel|maag|darm|darmen|villi|resorptie|koolhydraat|eiwit|vet|voedingsstof|glucose|glycogeen|zetmeel|cellulose"
    ],
    "Stofwisseling van de cel": [
        r"stofwisseling|celademhaling|glycolyse|krebscyclus|elektronentransport|ATP|ADP|NAD|FAD|mitochondri|chloroplast|fotosynthese|glucose|zuurstof|kooldioxide|energie|aerobe|anaerobe|melkzuur|gisting"
    ],
    "Bloedsomloop": [
        r"bloed|bloedsomloop|hart|slagader|ader|haarvat|capillair|bloedvat|bloeddruk|bloedplasma|rode bloedcel|witte bloedcel|bloedplaatje|hemoglobine|zuurstoftransport|kooldioxidetransport|hartslag|puls"
    ],
    "Ademhaling": [
        r"ademhaling|long|longen|alveoli|alveolus|luchtpijp|bronchus|bronchi|diafragma|borstholte|inademen|uitademen|zuurstof|O2|kooldioxide|CO2|gaswisseling|ademhalingscentrum"
    ],
    "Uitscheiding": [
        r"uitscheiding|nier|nieren|nefron|urine|blaas|ureum|ammoniak|lever|gal|ontgiftiging|transpiratie|zweten|huid"
    ],
    "Zenuwstelsel en hormonen": [
        r"zenuwstelsel|hersenen|ruggenmerg|zenuw|neuron|synaps|neurotransmitter|hormoon|hormonen|endocrien|hypofyse|bijnier|schildklier|alvleesklier|insuline|glucagon|adrenaline|testosteron|oestrogeen|progesteron|homeostase|reflex"
    ],
    "Waarnemen": [
        r"waarnemen|oog|netvlies|hoornvlies|lens|glasvocht|staafje|kegeltje|kleur|accommodatie|gehoor|oor|trommelvlies|gehoorbeentje|slakkenhuis|gehoorzenuw|reuk|smaak|tast|evenwicht"
    ],
    "Beweging": [
        r"beweging|spier|spieren|skelet|bot|beenderen|gewricht|pees|bewegingsstelsel|spiercontractie|actine|myosine|ATP|reflexboog"
    ],
    "Afweer": [
        r"afweer|immuunsysteem|witte bloedcel|lymfocyt|antistof|antigeen|vaccin|vaccinatie|infectie|ziekteverwekker|bacterie|virus|ontsteking|koorts|allergie|milt|lymfe|lymfeklier"
    ],
    "Erfelijkheid": [
        r"erfelijkheid|gen|genen|DNA|chromosoom|chromosomen|allel|allelen|homozygoot|heterozygoot|dominant|recessief|overerving|Mendel|kruising|stamboom|mutatie|genetische variatie|genetica|PCR"
    ],
    "Evolutie": [
        r"evolutie|natuurlijke selectie|Darwin|soortvorming|speciatie|adaptatie|aanpassing|variatie|selectiedruk|fitness|overleving|fortplanting|fylogenie|fossiel|genetische drift|genenstroom"
    ],
    "Ecologie": [
        r"ecologie|ecosysteem|populatie|gemeenschap|biotoop|abiotisch|biotisch|voedselketen|voedselweb|producent|consument|reductor|trofisch|energiestroom|koolstofkringloop|stikstofkringloop|symbiose|parasitisme|mutualisme|concurrentie|niche|habitat|biodiversiteit|milieu|vervuiling|klimaat"
    ],
    "Gedrag": [
        r"gedrag|ethologie|instinct|aangeleerd|conditionering|beloning|straf|imprinting|sociaal gedrag|groepsgedrag|hiërarchie|territorialiteit|communicatie|feromoon|agressie|voortplantingsgedrag|broedzorg"
    ],
    "Plantenfysiologie": [
        r"plant|planten|fotosynthese|chlorofyl|blad|bladeren|stengel|wortel|xyleem|floëem|houtvat|zeefvat|transpiratie|osmose|turgor|groei|hormoon|auxine|gibberelline|bloei|bestuiving|bevruchting|zaad|kieming"
    ]
}

# Nederlandse stopwoorden voor filtering
NEDERLANDS_STOPWOORDEN = [
    'het', 'de', 'een', 'en', 'van', 'in', 'op', 'te', 'dat', 'die', 'is', 'voor', 'met',
    'aan', 'als', 'hij', 'zij', 'wordt', 'door', 'ook', 'maar', 'om', 'na', 'zijn', 'er',
    'bij', 'op', 'uit', 'nog', 'al', 'dan', 'of', 'niet', 'wel', 'meest', 'veel', 'meer',
    'examen', 'vraag', 'biologie', 'havo', 'domein', 'opgave', 'figuur', 'tekst', 'afbeelding',
    'bepaal', 'noteer', 'schrijf', 'beschrijf', 'leg', 'uit', 'verklaar', 'geef', 'noem',
    'welke', 'wat', 'hoe', 'waarom', 'waar', 'wanneer', 'wie', 'hoeveel', 'hoelang'
]


def extract_dutch_text(pdf_text_file):
    """Extract Dutch text from PDF text file"""
    with open(pdf_text_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract text between [( and )] TJ
    matches = re.findall(r'\[(.*?)\] TJ', content)
    
    clean_lines = []
    for match in matches:
        # Check if match contains Dutch words
        has_dutch = any(woord.lower() in match.lower() for woord in NEDERLANDS_STOPWOORDEN)
        if not has_dutch:
            continue
        
        # Clean the match
        clean = re.sub(r'\[\\x[0-9a-fA-F]{2}\]', '', match)
        clean = re.sub(r'\([a-zA-Z0-9]+\)', '', clean)
        clean = re.sub(r'[\x00-\x1F\x7F-\xFF]', '', clean)
        clean = re.sub(r'[()\-]', ' ', clean)
        clean = re.sub(r'\s+', ' ', clean).strip()
        if clean and len(clean) > 5:
            clean_lines.append(clean)
    
    # Combine and final cleaning
    full_text = ' '.join(clean_lines)
    full_text = re.sub(r'\s+', ' ', full_text)
    # Remove numbers and special chars
    full_text = re.sub(r'[0-9\-]+', ' ', full_text)
    full_text = re.sub(r'[\x00-\x1F\x7F-\xFF]', '', full_text)
    full_text = re.sub(r'\s+', ' ', full_text).strip()
    
    return full_text


def identify_questions(text):
    """Identify questions based on keywords"""
    # Split into sentences (roughly)
    sentences = re.split(r'[.!?]', text)
    
    question_keywords = [
        'Noteer', 'Schrijf', 'Beschrijf', 'Leg uit', 'Verklaar', 'Geef',
        'Noem', 'Welke', 'Wat', 'Hoe', 'Waarom', 'Waar', 'Wanneer', 'Wie',
        'Hoeveel', 'Hoe lang', 'Is', 'Zijn', 'Heeft', 'Hebben', 'Kun',
        'Kan', 'Wordt', 'Worden', 'Geldt', 'Gelden', 'juist', 'onjuist',
        'waar', 'niet waar', 'correct', 'fout', 'Licht toe', 'Verklaar waarom',
        'Bepaal', 'Onderzoek', 'Toon aan', 'Bereken', 'Teken', 'Maak', 'Geef voorbeelden'
    ]
    
    questions = []
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence or len(sentence) < 10:
            continue
        
        # Check for question keywords
        for keyword in question_keywords:
            if keyword.lower() in sentence.lower():
                # Clean up
                q = re.sub(r'\s+', ' ', sentence)
                q = q.strip()
                if q and len(q) > 10 and q not in questions:
                    questions.append(q)
                break
    
    return questions


def categorize_question(question, domains=DOMEINEN):
    """Categorize a question by domain"""
    for domain, patterns in domains.items():
        for pattern in patterns:
            if re.search(pattern, question, re.IGNORECASE):
                return domain
    return "Onbekend"


def analyze_pdf(pdf_text_file):
    """Analyze a single PDF text file"""
    print(f"\n{'='*70}")
    print(f"Analyseren: {pdf_text_file}")
    print('='*70)
    
    # Extract text
    text = extract_dutch_text(pdf_text_file)
    print(f"Gereinigde tekst: {len(text)} karakters")
    
    # Identify questions
    questions = identify_questions(text)
    print(f"Gevonden vragen: {len(questions)}")
    
    # Categorize questions
    domain_questions = defaultdict(list)
    for q in questions:
        domain = categorize_question(q)
        domain_questions[domain].append(q)
    
    # Check which domains appear in text
    domain_in_text = set()
    for domain, patterns in DOMEINEN.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                domain_in_text.add(domain)
                break
    
    # Print results
    print("\n--- Domeinen in tekst ---")
    for domain in sorted(domain_in_text):
        print(f"  ✓ {domain}")
    
    print("\n--- Vragen per domein ---")
    for domain in sorted(domain_questions.keys()):
        qs = domain_questions[domain]
        if qs:
            print(f"\n{domain} ({len(qs)} vragen):")
            for i, q in enumerate(qs[:5], 1):
                display_q = q[:120] + "..." if len(q) > 120 else q
                print(f"  {i}. {display_q}")
            if len(qs) > 5:
                print(f"     ... en {len(qs) - 5} meer")
    
    return {
        'text_length': len(text),
        'questions': questions,
        'domain_questions': domain_questions,
        'domain_in_text': domain_in_text
    }


def main():
    pdf_files = ['2025I.txt', '2025I bijlage.txt', '2025II.txt']
    
    all_results = {}
    
    for pdf_file in pdf_files:
        try:
            results = analyze_pdf(pdf_file)
            all_results[pdf_file] = results
        except Exception as e:
            print(f"ERROR analyzing {pdf_file}: {e}")
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
    print("ALLE DOMEINEN DIE IN DE TEKSTEN VOORKOMEN")
    print("="*70)
    for domain in sorted(all_domains_found):
        print(f"  ✓ {domain}")
    
    # Save detailed results to file
    with open('analyse_resultaten.txt', 'w', encoding='utf-8') as f:
        f.write("EXAMENVRAAG ANALYSE - HAVO BIOLOGIE\n")
        f.write("="*70 + "\n\n")
        
        for pdf_file, results in all_results.items():
            f.write(f"\n{pdf_file}\n")
            f.write("-"*70 + "\n")
            f.write(f"Tekstlengte: {results['text_length']} karakters\n")
            f.write(f"Totaal vragen: {len(results['questions'])}\n\n")
            
            f.write("Vragen per domein:\n")
            for domain in sorted(results['domain_questions'].keys()):
                qs = results['domain_questions'][domain]
                if qs:
                    f.write(f"\n{domain} ({len(qs)} vragen):\n")
                    for i, q in enumerate(qs, 1):
                        f.write(f"  {i}. {q}\n")
    
    print("\n\nResultaten opgeslagen in: analyse_resultaten.txt")


if __name__ == '__main__':
    main()
