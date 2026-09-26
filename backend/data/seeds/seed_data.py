"""Seed reference dataset for CrisisPulse.
Provides realistic baseline conflict events and UN OCHA ReliefWeb humanitarian response data
for global crisis hotspots. Used as an offline seed, automated test fixture, and resilient fallback
when external APIs encounter upstream throttling (GDELT 429) or require pre-approved credentials (ReliefWeb v2).
"""

from typing import Dict, List, Any

GLOBAL_HOTSPOTS: List[Dict[str, Any]] = [
    {
        "region": "Sudan",
        "country_code": "SD",
        "lat": 12.8628,
        "lon": 30.2176,
        "gdelt_sample_headlines": [
            "Heavy artillery shelling reported across Khartoum and North Darfur",
            "Displacement crisis worsens as thousands cross Chad-Sudan border",
            "Famine conditions confirmed in Zamzam camp according to IPC alert",
            "Aid convoys blocked along key western transit corridors",
            "Emergency medical facilities overwhelmed amid conflict escalation"
        ],
        "tone_range": (-8.5, -4.2),
        "event_volume_24h": 480,
        "event_volume_7d": 2150,
        "reliefweb_reports": [
            {
                "id": "rw-sd-01",
                "title": "Sudan Humanitarian Response Situation Report No. 34",
                "source": "UN OCHA",
                "format": "Situation Report",
                "url": "https://reliefweb.int/report/sudan/sudan-humanitarian-response-sitrep-34"
            },
            {
                "id": "rw-sd-02",
                "title": "Sudan 2025 Revised Humanitarian Needs and Response Plan",
                "source": "UN OCHA",
                "format": "Appeal",
                "url": "https://reliefweb.int/report/sudan/sudan-humanitarian-needs-response-plan"
            }
        ],
        "reliefweb_response_count": 38
    },
    {
        "region": "Ukraine",
        "country_code": "UA",
        "lat": 48.3794,
        "lon": 31.1656,
        "gdelt_sample_headlines": [
            "Infrastructure damage reported following overnight drone and missile strikes",
            "Civilian evacuations underway in frontline settlements across Donetsk",
            "Emergency power grid repairs continue in Kharkiv and Dnipro",
            "Humanitarian partners deliver winterization supplies to eastern communities",
            "Diplomatic discussions on security guarantees continue in Geneva"
        ],
        "tone_range": (-6.8, -2.5),
        "event_volume_24h": 1250,
        "event_volume_7d": 8400,
        "reliefweb_reports": [
            {
                "id": "rw-ua-01",
                "title": "Ukraine: Humanitarian Impact and Response Update",
                "source": "UN OCHA",
                "format": "Situation Report",
                "url": "https://reliefweb.int/report/ukraine/humanitarian-impact-update"
            },
            {
                "id": "rw-ua-02",
                "title": "Ukraine Winter Response Plan 2025 Summary",
                "source": "UNHCR",
                "format": "Appeal",
                "url": "https://reliefweb.int/report/ukraine/winter-response-plan"
            }
        ],
        "reliefweb_response_count": 142
    },
    {
        "region": "Gaza (Palestine)",
        "country_code": "PS",
        "lat": 31.3547,
        "lon": 34.3088,
        "gdelt_sample_headlines": [
            "Airstrikes target central and southern governorates, critical casualties reported",
            "Severe malnutrition alerts issued by WHO as aid access remains constrained",
            "Temporary polio vaccination campaign completes second phase in Deir al-Balah",
            "Desalination and clean water infrastructure operating at minimal capacity",
            "International calls intensify for unimpeded humanitarian corridors"
        ],
        "tone_range": (-9.2, -5.0),
        "event_volume_24h": 1820,
        "event_volume_7d": 11400,
        "reliefweb_reports": [
            {
                "id": "rw-ps-01",
                "title": "Hostilities in the Gaza Strip and Israel - Flash Update",
                "source": "UN OCHA",
                "format": "Flash Appeal",
                "url": "https://reliefweb.int/report/occupied-palestinian-territory/flash-update"
            },
            {
                "id": "rw-ps-02",
                "title": "Gaza Strip Acute Food Insecurity Analysis - IPC Report",
                "source": "IPC",
                "format": "Assessment",
                "url": "https://reliefweb.int/report/occupied-palestinian-territory/ipc-report"
            }
        ],
        "reliefweb_response_count": 95
    },
    {
        "region": "Democratic Republic of the Congo",
        "country_code": "CD",
        "lat": -4.0383,
        "lon": 21.7587,
        "gdelt_sample_headlines": [
            "Clashes intensify around Sake and Goma in North Kivu province",
            "Mpox response efforts scaled up in South Kivu displacement camps",
            "Over 400,000 newly displaced in eastern DRC since January",
            "Militia attacks disrupt commercial and agricultural supply lines",
            "Peacekeepers reinforce defensive positions near civilian protection zones"
        ],
        "tone_range": (-7.4, -3.1),
        "event_volume_24h": 320,
        "event_volume_7d": 1890,
        "reliefweb_reports": [
            {
                "id": "rw-cd-01",
                "title": "DR Congo - Humanitarian Situation in North Kivu",
                "source": "UN OCHA",
                "format": "Situation Report",
                "url": "https://reliefweb.int/report/democratic-republic-congo/north-kivu-sitrep"
            }
        ],
        "reliefweb_response_count": 22
    },
    {
        "region": "Syria",
        "country_code": "SY",
        "lat": 34.8021,
        "lon": 38.9968,
        "gdelt_sample_headlines": [
            "Shelling reported along frontline villages in southern Idlib countryside",
            "Water scarcity and economic stagnation deepen vulnerability in Aleppo",
            "Cross-border humanitarian aid deliveries continue through Bab al-Hawa",
            "Severe fuel shortages affect emergency hospital operations",
            "Security incidents reported in northeastern displacement facilities"
        ],
        "tone_range": (-6.5, -2.8),
        "event_volume_24h": 410,
        "event_volume_7d": 2400,
        "reliefweb_reports": [
            {
                "id": "rw-sy-01",
                "title": "Northwest Syria Humanitarian Situation Report",
                "source": "UN OCHA",
                "format": "Situation Report",
                "url": "https://reliefweb.int/report/syrian-arab-republic/nw-syria-sitrep"
            }
        ],
        "reliefweb_response_count": 45
    },
    {
        "region": "Yemen",
        "country_code": "YE",
        "lat": 15.5527,
        "lon": 48.5164,
        "gdelt_sample_headlines": [
            "Naval security incidents reported in southern Red Sea shipping lanes",
            "Flash floods destroy shelters in Hodeidah and Marib displacement sites",
            "Cholera caseloads rise amid strained sanitation systems",
            "UN agencies call for release of detained humanitarian personnel",
            "Currency depreciation drives staple food prices to record highs"
        ],
        "tone_range": (-7.1, -3.5),
        "event_volume_24h": 390,
        "event_volume_7d": 2100,
        "reliefweb_reports": [
            {
                "id": "rw-ye-01",
                "title": "Yemen Humanitarian Update - Issue 7",
                "source": "UN OCHA",
                "format": "Situation Report",
                "url": "https://reliefweb.int/report/yemen/humanitarian-update-issue-7"
            }
        ],
        "reliefweb_response_count": 29
    },
    {
        "region": "Myanmar",
        "country_code": "MM",
        "lat": 21.9162,
        "lon": 95.9560,
        "gdelt_sample_headlines": [
            "Armed resistance clashes with military forces across northern Shan State",
            "Typhoon flood aftermath compounds humanitarian crisis in central valleys",
            "Telecom blackouts reported in contested townships of Rakhine State",
            "Banking restrictions and currency volatility disrupt aid procurement",
            "Border trade routes remain largely suspended due to active hostilities"
        ],
        "tone_range": (-8.0, -3.9),
        "event_volume_24h": 260,
        "event_volume_7d": 1650,
        "reliefweb_reports": [
            {
                "id": "rw-mm-01",
                "title": "Myanmar Humanitarian Update - Flash Update No. 8",
                "source": "UN OCHA",
                "format": "Flash Update",
                "url": "https://reliefweb.int/report/myanmar/myanmar-update-flash-8"
            }
        ],
        "reliefweb_response_count": 16
    },
    {
        "region": "Haiti",
        "country_code": "HT",
        "lat": 18.9712,
        "lon": -72.2852,
        "gdelt_sample_headlines": [
            "Gang violence expands into residential neighborhoods of Port-au-Prince",
            "Multinational Security Support mission conducts joint patrols with national police",
            "Displaced families shelter in makeshift classrooms as schools remain closed",
            "Fuel and supply shortages hit general hospitals in metropolitan area",
            "Port logistics slowly resume under tight security cordons"
        ],
        "tone_range": (-8.7, -4.5),
        "event_volume_24h": 310,
        "event_volume_7d": 1920,
        "reliefweb_reports": [
            {
                "id": "rw-ht-01",
                "title": "Haiti: Escalation of Violence Flash Update No. 12",
                "source": "UN OCHA",
                "format": "Flash Update",
                "url": "https://reliefweb.int/report/haiti/escalation-violence-flash-12"
            }
        ],
        "reliefweb_response_count": 14
    },
    {
        "region": "Somalia",
        "country_code": "SO",
        "lat": 5.1521,
        "lon": 46.1996,
        "gdelt_sample_headlines": [
            "Military operations continue against insurgent stronghold in Galmudug",
            "Localized drought alerts issued following erratic seasonal rains",
            "Humanitarian actors scale up nutrition clinics in Baidoa camps",
            "Inter-communal mediation efforts underway in central regions",
            "Cash assistance programs expanded to mitigate acute food insecurity"
        ],
        "tone_range": (-6.2, -2.4),
        "event_volume_24h": 180,
        "event_volume_7d": 1200,
        "reliefweb_reports": [
            {
                "id": "rw-so-01",
                "title": "Somalia Humanitarian Situation Report",
                "source": "UN OCHA",
                "format": "Situation Report",
                "url": "https://reliefweb.int/report/somalia/humanitarian-sitrep"
            }
        ],
        "reliefweb_response_count": 25
    },
    {
        "region": "Afghanistan",
        "country_code": "AF",
        "lat": 33.9391,
        "lon": 67.7100,
        "gdelt_sample_headlines": [
            "Severe economic strain impacts rural livelihoods ahead of winter season",
            "Earthquake reconstruction assistance continues in western provinces",
            "Female aid worker restrictions continue to challenge operational delivery",
            "Border crossings with Pakistan face intermittent commercial closures",
            "Malnutrition treatment centers report steady influx of pediatric patients"
        ],
        "tone_range": (-6.9, -3.0),
        "event_volume_24h": 220,
        "event_volume_7d": 1480,
        "reliefweb_reports": [
            {
                "id": "rw-af-01",
                "title": "Afghanistan Humanitarian Needs and Response Overview",
                "source": "UN OCHA",
                "format": "Appeal",
                "url": "https://reliefweb.int/report/afghanistan/humanitarian-needs-overview"
            }
        ],
        "reliefweb_response_count": 31
    }
]
