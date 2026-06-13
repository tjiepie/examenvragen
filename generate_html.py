#!/usr/bin/env python3
"""
Script om een interactieve HTML-pagina te genereren met zoekfunctie
voor examenvragen per domein.
"""

import csv
import json

# Lees de CSV met vragen
questions = []
with open('examenvragen_complete.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        questions.append({
            'pdf': row['PDF Bestandsnaam'],
            'domain': row['Domein'],
            'question': row['Vraag']
        })

# Domein statistieken
domain_counts = {}
for q in questions:
    domain = q['domain']
    domain_counts[domain] = domain_counts.get(domain, 0) + 1

# HTML template
html_template = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Examenvragen HAVO Biologie - Domeinen Overzicht</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f7fa;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        header {{
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            padding: 30px 0;
            text-align: center;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .stats-overview {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .stat-card h3 {{
            color: #2c3e50;
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        
        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #3498db;
        }}
        
        .stat-card .percentage {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        .search-section {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        .search-section h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.5em;
        }}
        
        .search-controls {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .search-input {{
            flex: 1;
            min-width: 250px;
            padding: 12px 20px;
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 1em;
            transition: border-color 0.3s ease;
        }}
        
        .search-input:focus {{
            outline: none;
            border-color: #3498db;
        }}
        
        .filter-select {{
            padding: 12px 20px;
            border: 2px solid #ddd;
            border-radius: 25px;
            font-size: 1em;
            background: white;
            cursor: pointer;
            transition: border-color 0.3s ease;
        }}
        
        .filter-select:focus {{
            outline: none;
            border-color: #3498db;
        }}
        
        .results-count {{
            margin-top: 15px;
            color: #7f8c8d;
            font-size: 0.95em;
        }}
        
        .domain-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .domain-link {{
            display: block;
            padding: 15px;
            background: white;
            border: 2px solid #ddd;
            border-radius: 10px;
            text-decoration: none;
            color: #2c3e50;
            transition: all 0.3s ease;
            text-align: center;
        }}
        
        .domain-link:hover {{
            background: #3498db;
            color: white;
            border-color: #3498db;
            transform: translateY(-3px);
        }}
        
        .domain-link h4 {{
            margin-bottom: 5px;
        }}
        
        .domain-link .count {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        
        .question-item {{
            padding: 15px;
            margin-bottom: 10px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #bdc3c7;
            transition: all 0.3s ease;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .question-item:hover {{
            background: #f0f4f8;
            border-left-color: #3498db;
            transform: translateX(5px);
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }}
        
        .question-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        
        .question-domain {{
            background: #3498db;
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        
        .question-pdf {{
            background: #e74c3c;
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85em;
        }}
        
        .question-text {{
            color: #34495e;
            line-height: 1.6;
            margin-top: 8px;
        }}
        
        .no-results {{
            text-align: center;
            padding: 40px;
            color: #7f8c8d;
            font-size: 1.1em;
        }}
        
        .highlight {{
            background-color: #ffeb3b;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        
        @media (max-width: 768px) {{
            .search-controls {{
                flex-direction: column;
                align-items: stretch;
            }}
            
            .search-input, .filter-select {{
                width: 100%;
            }}
            
            .domain-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .back-to-top {{
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: all 0.3s ease;
        }}
        
        .back-to-top:hover {{
            background: #2980b9;
            transform: translateY(-2px);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 Examenvragen HAVO Biologie</h1>
            <p>Domeinen Overzicht - 2025 Examens</p>
        </header>
        
        <section class="stats-overview">
            <div class="stat-card">
                <h3>Totaal Vragen</h3>
                <div class="number">{len(questions)}</div>
                <div class="percentage">100%</div>
            </div>
            <div class="stat-card">
                <h3>Domeinen</h3>
                <div class="number">{len(domain_counts)}</div>
                <div class="percentage">actief</div>
            </div>
            <div class="stat-card">
                <h3>Examens</h3>
                <div class="number">3</div>
                <div class="percentage">2025 I & II</div>
            </div>
            <div class="stat-card">
                <h3>Gecategoriseerd</h3>
                <div class="number">{sum(domain_counts.values())}</div>
                <div class="percentage">{sum(domain_counts.values())/len(questions)*100:.1f}%</div>
            </div>
        </section>
        
        <section class="search-section">
            <h2>🔍 Zoek en Filter Vragen</h2>
            <div class="search-controls">
                <input type="text" id="search-input" class="search-input" placeholder="Zoek in vragen...">
                <select id="domain-filter" class="filter-select">
                    <option value="">Alle Domeinen</option>
"""

# Add domain options
for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / len(questions)) * 100
    html_template += f'                    <option value="{domain}">{domain} ({count} - {percentage:.1f}%)</option>\n'

html_template += """                </select>
                <select id="pdf-filter" class="filter-select">
                    <option value="">Alle Examens</option>
                    <option value="2025I.pdf">2025 Tijdvak 1</option>
                    <option value="2025I bijlage.pdf">2025 Tijdvak 1 Bijlage</option>
                    <option value="2025II.pdf">2025 Tijdvak 2</option>
                </select>
            </div>
            <div class="results-count" id="results-count"></div>
        </section>
        
        <section id="domain-overview">
            <h2 style="color: #2c3e50; margin-bottom: 20px;">📊 Domeinen Overzicht</h2>
            <div class="domain-grid" id="domain-grid">
"""

# Add domain links
for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / len(questions)) * 100
    html_template += f'''                <a href="#{domain}" class="domain-link">
                    <h4>{domain}</h4>
                    <div class="count">{count} vragen ({percentage:.1f}%)</div>
                </a>
'''

html_template += """            </div>
        </section>
        
        <section id="questions-container">
            <!-- Questions will be inserted here by JavaScript -->
        </section>
        
        <a href="#" class="back-to-top" onclick="window.scrollTo({top: 0, behavior: 'smooth'}); return false;">🔝 Terug naar boven</a>
    </div>
    
    <script>
        // Questions data
        const questionsData = """

# Convert questions to JSON
questions_json = json.dumps(questions, ensure_ascii=False, indent=4)
html_template += questions_json

html_template += """";
        
        // Filter and display functions
        function filterQuestions() {
            const searchTerm = document.getElementById('search-input').value.toLowerCase();
            const domainFilter = document.getElementById('domain-filter').value;
            const pdfFilter = document.getElementById('pdf-filter').value;
            
            const filtered = questionsData.filter(q => {
                const matchesSearch = !searchTerm || q.question.toLowerCase().includes(searchTerm);
                const matchesDomain = !domainFilter || q.domain === domainFilter;
                const matchesPdf = !pdfFilter || q.pdf === pdfFilter;
                return matchesSearch && matchesDomain && matchesPdf;
            });
            
            displayQuestions(filtered);
            updateResultsCount(filtered.length);
        }
        
        function displayQuestions(questions) {
            const container = document.getElementById('questions-container');
            
            if (questions.length === 0) {
                container.innerHTML = '<div class="no-results">Geen vragen gevonden die voldoen aan de criteria.</div>';
                return;
            }
            
            // Group by domain
            const grouped = {};
            questions.forEach(q => {
                if (!grouped[q.domain]) grouped[q.domain] = [];
                grouped[q.domain].push(q);
            });
            
            let html = '';
            for (const [domain, domainQuestions] of Object.entries(grouped)) {
                html += `<div class="domain-section" id="${domain}">`;
                html += `<div class="domain-header">`;
                html += `<h3>${domain}</h3>`;
                html += `<span class="domain-badge">${domainQuestions.length} vragen</span>`;
                html += `</div>`;
                html += `<ul class="question-list">`;
                
                domainQuestions.forEach(q => {
                    html += `<li class="question-item">`;
                    html += `<div class="question-header">`;
                    html += `<span class="question-domain">${q.domain}</span>`;
                    html += `<span class="question-pdf">${q.pdf.replace('.pdf', '')}</span>`;
                    html += `</div>`;
                    html += `<div class="question-text">${q.question}</div>`;
                    html += `</li>`;
                });
                
                html += `</ul>`;
                html += `</div>`;
            }
            
            container.innerHTML = html;
        }
        
        function updateResultsCount(count) {
            const total = questionsData.length;
            document.getElementById('results-count').textContent = 
                `Gevonden: ${count} van ${total} vragen`;
        }
        
        // Event listeners
        document.getElementById('search-input').addEventListener('input', filterQuestions);
        document.getElementById('domain-filter').addEventListener('change', filterQuestions);
        document.getElementById('pdf-filter').addEventListener('change', filterQuestions);
        
        // Initial display
        displayQuestions(questionsData);
        updateResultsCount(questionsData.length);
        
        // Smooth scroll for domain links
        document.querySelectorAll('.domain-link').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const domain = this.getAttribute('href').substring(1);
                const element = document.getElementById(domain);
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    </script>
</body>
</html>
"""

# Write the HTML file
with open('examenvragen_interactief.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"HTML-bestand gegenereerd: examenvragen_interactief.html")
print(f"Totaal: {len(questions)} vragen")
print(f"Domeinen: {len(domain_counts)}")
for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / len(questions)) * 100
    print(f"  {domain}: {count} ({percentage:.1f}%)")
