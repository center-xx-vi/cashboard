import json


def create_switching_website(json_file, gif_url):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Fehler: {json_file} nicht gefunden.")
        return

    members = data[:25]
    monate_namen = [
        "Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember"
    ]

    html_content = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Dynamic Performance Matrix</title>
        <style>
            body {{
                background-image: url('{gif_url}');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                margin: 0;
                overflow-x: hidden;
            }}
            .bg-overlay {{ background-color: rgba(0, 0, 0, 0.75); min-height: 100vh; width: 100vw; }}
            .compact-cell {{ width: calc(100vw / 26.5); min-width: 0; }}

            .mode-netto .val-brutto {{ display: none; }}
            .mode-brutto .val-netto {{ display: none; }}

            .active-label {{
                transition: all 0.3s ease;
            }}
        </style>
    </head>
    <body class="text-white font-sans text-[10px] mode-netto" id="main-body">
        <div class="bg-overlay py-4 px-2">
            <header class="flex justify-between items-center max-w-[98vw] mx-auto mb-4">
                <h1 class="text-lg font-black uppercase tracking-[0.3em] text-emerald-400">Team Dashboard 2026</h1>

                <div class="flex gap-4 items-center bg-black/40 px-4 py-2 rounded-full border border-white/10">
                    <span id="label-netto" class="uppercase font-bold tracking-widest text-emerald-400 opacity-100 transition-opacity">Netto-Ansicht</span>
                    <span class="text-gray-600">|</span>
                    <span id="label-brutto" class="uppercase font-bold tracking-widest text-amber-500 opacity-30 transition-opacity">Brutto-Ansicht</span>
                </div>
            </header>

            <div class="w-full bg-black/40 backdrop-blur-3xl rounded-xl border border-white/10 shadow-2xl overflow-hidden">
                <table class="w-full table-fixed border-collapse">
                    <thead>
                        <tr class="bg-white/10">
                            <th class="w-16 p-2 border-r border-white/10 uppercase font-bold text-gray-500">Monat</th>
                            {" ".join([f'''
                            <th class="p-1 border-r border-white/10 text-center compact-cell">
                                <img src="https://ui-avatars.com/api/?name={m['name'].replace(" ", "+")}&background=random&color=fff&size=40" 
                                     class="w-6 h-6 rounded-full mx-auto mb-1 border border-white/20">
                                <div class="text-[7px] font-bold uppercase truncate overflow-hidden whitespace-nowrap px-1">{m['name'].split()[0]}</div>
                            </th>''' for m in members])}
                        </tr>
                    </thead>
                    <tbody>
    """

    for idx, monat in enumerate(monate_namen):
        html_content += f"""
                        <tr class="border-b border-white/5 hover:bg-white/5 transition-all">
                            <td class="p-2 font-bold border-r border-white/10 bg-black/20 text-center text-gray-400">
                                {monat[:3]}
                            </td>
        """
        for m in members:
            n_val = m.get("netto_monate", [])[idx] if idx < len(m.get("netto_monate", [])) else 0
            b_val = m.get("brutto_monate", [])[idx] if idx < len(m.get("brutto_monate", [])) else 0

            html_content += f"""
                            <td class="p-2 border-r border-white/10 text-center compact-cell font-bold text-[11px]">
                                <span class="val-netto text-emerald-300">{n_val}</span>
                                <span class="val-brutto text-amber-400">{b_val}</span>
                            </td>
            """
        html_content += "</tr>"

    html_content += """
                        <tr class="bg-white/5 border-t-2 border-white/20">
                            <td class="p-2 font-black border-r border-white/10 text-center text-white uppercase tracking-tighter">
                                TOTAL
                            </td>
    """
    for m in members:
        s_netto = sum(m.get("netto_monate", []))
        s_brutto = sum(m.get("brutto_monate", []))
        html_content += f"""
                            <td class="p-2 border-r border-white/10 text-center compact-cell font-black text-[11px]">
                                <span class="val-netto text-emerald-400">{s_netto}</span>
                                <span class="val-brutto text-amber-500">{s_brutto}</span>
                            </td>
        """

    html_content += """
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="mt-8 flex flex-col items-center">
                <div class="bg-black/50 backdrop-blur-md p-4 rounded-2xl border border-yellow-500/30 shadow-[0_0_20px_rgba(234,179,8,0.2)] text-center">
                    <h2 class="text-yellow-500 font-black uppercase tracking-[0.5em] mb-3 text-xs italic">Employee of the Month</h2>
                    <img src="employee_of_the_month.png" alt="Employee of the Month" 
                         class="w-48 h-auto rounded-lg border-2 border-yellow-500/50 shadow-lg mx-auto overflow-hidden">
                </div>
            </div>

        </div>

        <script>
            const body = document.getElementById('main-body');
            const lNetto = document.getElementById('label-netto');
            const lBrutto = document.getElementById('label-brutto');

            setInterval(() => {
                if (body.classList.contains('mode-netto')) {
                    body.classList.remove('mode-netto');
                    body.classList.add('mode-brutto');
                    lNetto.style.opacity = "0.3";
                    lBrutto.style.opacity = "1";
                } else {
                    body.classList.remove('mode-brutto');
                    body.classList.add('mode-netto');
                    lNetto.style.opacity = "1";
                    lBrutto.style.opacity = "0.3";
                }
            }, 10000);
        </script>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Website mit 'Employee of the Month' Bild wurde erstellt!")


GIF_URL = "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExaG44eXVpMHh1c2xvbnA4bGUydHA5MWZydXE0djIzYTkwaG8wc281MiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JpG2A9P3dPHXaTYrwu/giphy.gif"
create_switching_website("data.json", GIF_URL)