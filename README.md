# otorongo-scraper

> Scrapy spider that extracts candidate profiles from [otorongo.club](https://otorongo.club) — a Peruvian civic platform that aggregates public records (criminal backgrounds, education, work history, political experience) for congressional and regional election candidates.

Originally built for the 2021 and 2022 elections; updated to target the 2026 election cycle.

## What it does

- **Spider** (`radar_scraper/spiders/otorongo.py`) — crawls candidate listing pages for 2021 and 2022, follows each profile link, and extracts: name, DNI, birth date, address, political party, running city/position, education levels, criminal backgrounds, work experience, and party history.
- **Pipeline** (`pipelines.py`) — normalizes whitespace, formats birth place strings, and cleans nested arrays before export.
- **Middlewares** (`middlewares.py`) — rotates fake browser headers via ScrapeOps, deduplicates requests with logging, and saves error URLs to `error_urls.txt` on close.
- **Output** — writes `candidates_otorongo.json` (one JSON array, UTF-8).

## Stack

Python 3.10+ · Scrapy 2.x · python-dotenv · ScrapeOps (optional, for header rotation)

## Local setup

```bash
git clone https://github.com/RayverAimar/otorongo-scraper.git
cd otorongo-scraper/radar_scraper

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install scrapy python-dotenv requests
```

## Environment variables

Create a `.env` file inside `radar_scraper/`:

```
SCRAPE_OPS_API_KEY=your_key_here
```

Get a free key at [scrapeops.io](https://scrapeops.io). Without it the `ScrapeOpsFakeBrowserMiddleware` is disabled automatically and Scrapy uses its default headers.

## Run

```bash
cd radar_scraper
scrapy crawl otorongo
```

The spider crawls both election years concurrently and writes results to `candidates_otorongo.json` in the current directory. Duplicate requests are logged to `duplicated_requests.txt` and HTTP errors to `error_urls.txt`.

## Output

`candidates_otorongo.json` — one object per candidate:

```json
[
  {
    "name": "ROBERD EDDIE NAVARRO MENDOZA",
    "dni": "31009114",
    "birth_date": "11/03/1966",
    "home_address": "ABANCAY, APURIMAC.",
    "birth_place": "PERÚ, APURIMAC, ABANCAY, ABANCAY",
    "political_party": "PARTIDO POLITICO INTEGRIDAD DEMOCRATICA",
    "running_position": "DIPUTADO (Nro. 1)",
    "running_city": "APURIMAC",
    "school_studies": ["Primaria: Sí - Completa", "Secundaria: Sí - Completa"],
    "technical_education": "POLICIA NACIONAL - POLICIA NACIONAL",
    "non_university_education": "-",
    "university_education": [
      "Universidad Tecnológica de los Andes - BACHILLER EN DERECHO - 2019 - Completa.",
      "Universidad Tecnológica de los Andes - ABOGADO - 2022 - Completa."
    ],
    "postgraduate_studies": [],
    "other_postgraduate_studies": [],
    "background_intentional_crimes": [
      {
        "No de Expediente": "00111-2025-0-0301-JR-PE-01",
        "Fecha antecedente firme": "21/10/2021",
        "Órgano judicial": "JUZGADO PENAL SUPERPROVINCIAL",
        "Delito": "APROPIADO ILICITO",
        "Fallo o pena": "ARCHIVADO PRESCRITA",
        "Modalidad": "SUSPENDIDA",
        "Otra modalidad": "None",
        "Cumplimiento del fallo": "PENA CUMPLIDA"
      }
    ],
    "background_legal_confirmed": [
      {
        "Materia de la demanda": "FAMILIA / ALIMENTARIA",
        "No de Expediente": "00221-1997-18-JP-FP-04",
        "Órgano judicial": "4 JUZGADO DE PAZ LETRADO LIMA",
        "Fallo/pena": "ARCHIVADO"
      }
    ],
    "work_experience": [
      { "time_lapse": "2019 - 2025", "info": "ABOGADO - CORPORACION LEX" }
    ],
    "additional_information": "-",
    "political_experience": [
      { "time_lapse": "2024 - 2024", "info": "DIPUTADO - PARTIDO POLÍTICO PARTIDO POLITICO INTEGRIDAD DEMOCRATICA" }
    ],
    "party_history": [
      { "time_lapse": "2024 - 2025", "info": "SECRETARIO GENERAL PROVINCIAL - PARTIDO POLÍTICO PARTIDO POLITICO INTEGRIDAD DEMOCRATICA" }
    ],
    "year": "2026"
  }
]
```

## License

MIT
