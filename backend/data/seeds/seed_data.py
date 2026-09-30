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
                "title": "Sudan Humanitarian Response Situation Report",
                "source": "UN OCHA",
                "format": "Situation Report",
                "url": "https://reliefweb.int/country/sdn"
            },
            {
                "id": "rw-sd-02",
                "title": "Sudan Humanitarian Needs and Response Plan",
                "source": "UN OCHA",
                "format": "Appeal",
                "url": "https://reliefweb.int/country/sdn"
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
                "url": "https://reliefweb.int/country/ukr"
            },
            {
                "id": "rw-ua-02",
                "title": "Ukraine Winter Response Plan Summary",
                "source": "UNHCR",
                "format": "Appeal",
                "url": "https://reliefweb.int/country/ukr"
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
                "title": "Occupied Palestinian Territory: Hostilities Flash Update",
                "source": "UN OCHA",
                "format": "Flash Appeal",
                "url": "https://reliefweb.int/country/pse"
            },
            {
                "id": "rw-ps-02",
                "title": "Gaza Strip Acute Food Insecurity Analysis - IPC Report",
                "source": "IPC",
                "format": "Assessment",
                "url": "https://reliefweb.int/country/pse"
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
                "title": "DR Congo - Humanitarian Situation in Eastern Provinces",
                "source": "UN OCHA",
                "format": "Situation Report",
                "url": "https://reliefweb.int/country/cod"
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
                "title": "Syria Humanitarian Situation Report",
                "source": "UN OCHA",
                "format": "Situation Report",
                "url": "https://reliefweb.int/country/syr"
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
                "title": "Yemen Humanitarian Update",
                "source": "UN OCHA",
                "format": "Situation Report",
                "url": "https://reliefweb.int/country/yem"
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
                "title": "Myanmar Humanitarian Update",
                "source": "UN OCHA",
                "format": "Flash Update",
                "url": "https://reliefweb.int/country/mmr"
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
                "title": "Haiti: Escalation of Violence Flash Update",
                "source": "UN OCHA",
                "format": "Flash Update",
                "url": "https://reliefweb.int/country/hti"
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
                "url": "https://reliefweb.int/country/som"
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
                "url": "https://reliefweb.int/country/afg"
            }
        ],
        "reliefweb_response_count": 31
    },
    {
        "region": "Ethiopia",
        "country_code": "ET",
        "lat": 9.1450,
        "lon": 40.4897,
        "gdelt_sample_headlines": [
            "Food distribution resumes in Amhara and Tigray amidst fragile ceasefire",
            "Clashes in Oromia region displace thousands of farming families",
            "Severe malnutrition survey indicates alarming thresholds in Somali regional state"
        ],
        "tone_range": (-6.5, -2.8),
        "event_volume_24h": 290,
        "event_volume_7d": 1820,
        "reliefweb_reports": [{"id": "rw-et-01", "title": "Ethiopia Humanitarian Situation Update", "source": "UN OCHA", "format": "Situation Report", "url": "https://reliefweb.int/country/eth"}],
        "reliefweb_response_count": 34
    },
    {
        "region": "South Sudan",
        "country_code": "SS",
        "lat": 6.8770,
        "lon": 31.3070,
        "gdelt_sample_headlines": [
            "Unprecedented seasonal flooding cuts off entire counties in Unity and Jonglei states",
            "Returnees fleeing Sudan war strain border transit center resources",
            "Cholera outbreak declared in Upper Nile state transit hubs"
        ],
        "tone_range": (-7.4, -3.5),
        "event_volume_24h": 230,
        "event_volume_7d": 1390,
        "reliefweb_reports": [{"id": "rw-ss-01", "title": "South Sudan Crisis Response", "source": "UN OCHA", "format": "Situation Report", "url": "https://reliefweb.int/country/ssd"}],
        "reliefweb_response_count": 28
    },
    {
        "region": "Burkina Faso",
        "country_code": "BF",
        "lat": 12.2383,
        "lon": -1.5616,
        "gdelt_sample_headlines": [
            "Blockaded northern towns face critical shortages of staple foods and medicine",
            "Security forces clash with armed groups in Sahel and Centre-Nord regions",
            "Aid airdrops provide temporary sustenance to isolated communities"
        ],
        "tone_range": (-8.1, -4.0),
        "event_volume_24h": 310,
        "event_volume_7d": 1640,
        "reliefweb_reports": [{"id": "rw-bf-01", "title": "Burkina Faso Humanitarian Emergency", "source": "UN OCHA", "format": "Situation Report", "url": "https://reliefweb.int/country/bfa"}],
        "reliefweb_response_count": 19
    },
    {
        "region": "Mali",
        "country_code": "ML",
        "lat": 17.5707,
        "lon": -3.9962,
        "gdelt_sample_headlines": [
            "Heavy clashes reported in northern Kidal and Gao sectors",
            "Drone strikes hit militant convoys near Niger border",
            "Fuel shortages disrupt humanitarian transport operations across Mopti"
        ],
        "tone_range": (-7.2, -3.1),
        "event_volume_24h": 260,
        "event_volume_7d": 1510,
        "reliefweb_reports": [{"id": "rw-ml-01", "title": "Mali Situation Report", "source": "UN OCHA", "format": "Situation Report", "url": "https://reliefweb.int/country/mli"}],
        "reliefweb_response_count": 22
    },
    {
        "region": "Niger",
        "country_code": "NE",
        "lat": 17.6078,
        "lon": 8.0817,
        "gdelt_sample_headlines": [
            "Tillabéri border region tensions trigger secondary displacements",
            "Severe flooding damages mud-brick housing and crops along River Niger",
            "Sanctions easing restores limited cross-border medical imports"
        ],
        "tone_range": (-5.8, -2.0),
        "event_volume_24h": 170,
        "event_volume_7d": 1100,
        "reliefweb_reports": [{"id": "rw-ne-01", "title": "Niger Humanitarian Dashboard", "source": "UN OCHA", "format": "Situation Report", "url": "https://reliefweb.int/country/ner"}],
        "reliefweb_response_count": 18
    },
    {
        "region": "Nigeria (North-East & Sahel)",
        "country_code": "NG",
        "lat": 9.0820,
        "lon": 8.6753,
        "gdelt_sample_headlines": [
            "Insurgent ambushes reported in Lake Chad basin fringe communities",
            "Banditry and mass abductions in Zamfara and Katsina displace farming hamlets",
            "Floods submerge Maiduguri city triggering massive public health emergency"
        ],
        "tone_range": (-6.9, -2.5),
        "event_volume_24h": 410,
        "event_volume_7d": 2400,
        "reliefweb_reports": [{"id": "rw-ng-01", "title": "Nigeria Humanitarian Overview", "source": "UN OCHA", "format": "Situation Report", "url": "https://reliefweb.int/country/nga"}],
        "reliefweb_response_count": 42
    },
    {
        "region": "Chad",
        "country_code": "TD",
        "lat": 15.4542,
        "lon": 18.7322,
        "gdelt_sample_headlines": [
            "Over 650,000 Sudanese refugees hosted in eastern provinces under intense water strain",
            "Torrential rains wash out vital bridge crossings linking Adre to N'Djamena",
            "Emergency measles vaccination campaigns launched in transit settlement camps"
        ],
        "tone_range": (-6.3, -2.1),
        "event_volume_24h": 190,
        "event_volume_7d": 1150,
        "reliefweb_reports": [{"id": "rw-td-01", "title": "Chad Refugee Emergency Update", "source": "UNHCR", "format": "Situation Report", "url": "https://reliefweb.int/country/tcd"}],
        "reliefweb_response_count": 27
    },
    {
        "region": "Central African Republic",
        "country_code": "CF",
        "lat": 6.6111,
        "lon": 20.9394,
        "gdelt_sample_headlines": [
            "Armed group extortion halts commercial supply corridors from Cameroon border",
            "Inter-ethnic skirmishes reported near diamond mining zones in Ouham",
            "Funding shortfall jeopardizes basic primary healthcare delivery across rural prefectures"
        ],
        "tone_range": (-6.4, -2.3),
        "event_volume_24h": 120,
        "event_volume_7d": 840,
        "reliefweb_reports": [{"id": "rw-cf-01", "title": "CAR Humanitarian Bulletin", "source": "UN OCHA", "format": "Situation Report", "url": "https://reliefweb.int/country/caf"}],
        "reliefweb_response_count": 16
    },
    {
        "region": "Mozambique (Cabo Delgado)",
        "country_code": "MZ",
        "lat": -18.6657,
        "lon": 35.5296,
        "gdelt_sample_headlines": [
            "Insurgent raids on coastal towns in Cabo Delgado spark coastal canoe evacuations",
            "Multinational regional forces conduct clearance operations near Palma",
            "Cholera vaccination scaled up following cyclone-induced infrastructure damage"
        ],
        "tone_range": (-6.5, -2.7),
        "event_volume_24h": 160,
        "event_volume_7d": 980,
        "reliefweb_reports": [{"id": "rw-mz-01", "title": "Mozambique Cabo Delgado Flash Update", "source": "UN OCHA", "format": "Situation Report", "url": "https://reliefweb.int/country/moz"}],
        "reliefweb_response_count": 21
    },
    {
        "region": "Lebanon",
        "country_code": "LB",
        "lat": 33.8547,
        "lon": 35.8623,
        "gdelt_sample_headlines": [
            "Intense airstrikes hit southern suburbs of Beirut and Bekaa Valley",
            "Over 1.2 million individuals displaced seeking temporary shelter in schools",
            "Hospitals report extreme shortages of trauma and surgical supply kits"
        ],
        "tone_range": (-8.6, -4.5),
        "event_volume_24h": 1420,
        "event_volume_7d": 6800,
        "reliefweb_reports": [{"id": "rw-lb-01", "title": "Lebanon Emergency Flash Appeal", "source": "UN OCHA", "format": "Appeal", "url": "https://reliefweb.int/country/lbn"}],
        "reliefweb_response_count": 78
    },
    {
        "region": "Iraq",
        "country_code": "IQ",
        "lat": 33.2232,
        "lon": 43.6793,
        "gdelt_sample_headlines": [
            "Severe water scarcity in southern marshlands triggers climate migration to Basra",
            "Militia standoff and drone alerts reported along western desert sectors",
            "Unexploded ordnance clearance programs continue in Sinjar and Mosul outskirts"
        ],
        "tone_range": (-4.9, -1.8),
        "event_volume_24h": 280,
        "event_volume_7d": 1950,
        "reliefweb_reports": [{"id": "rw-iq-01", "title": "Iraq Post-Conflict Transition Report", "source": "UN OCHA", "format": "Situation Report", "url": "https://reliefweb.int/country/irq"}],
        "reliefweb_response_count": 36
    },
    {
        "region": "Pakistan (Balochistan & KPK)",
        "country_code": "PK",
        "lat": 30.3753,
        "lon": 69.3451,
        "gdelt_sample_headlines": [
            "Coordinated insurgent attacks hit highway checkpoints across Balochistan",
            "Militant clashes reported along northwestern Afghan border zones",
            "Relief operations provide winter kits to flood-affected districts in Sindh"
        ],
        "tone_range": (-6.8, -2.6),
        "event_volume_24h": 380,
        "event_volume_7d": 2100,
        "reliefweb_reports": [{"id": "rw-pk-01", "title": "Pakistan Emergency Overview", "source": "UN OCHA", "format": "Situation Report", "url": "https://reliefweb.int/country/pak"}],
        "reliefweb_response_count": 29
    },
    {
        "region": "Libya",
        "country_code": "LY",
        "lat": 26.3351,
        "lon": 17.2283,
        "gdelt_sample_headlines": [
            "Rival military mobilizations around Tripoli raise security alert levels",
            "Derna dam reconstruction proceeds slowly amidst political division",
            "Migrant detention center conditions face scrutiny by UN human rights experts"
        ],
        "tone_range": (-5.2, -1.9),
        "event_volume_24h": 160,
        "event_volume_7d": 1120,
        "reliefweb_reports": [{"id": "rw-ly-01", "title": "Libya Humanitarian Flash Update", "source": "UN OCHA", "format": "Situation Report", "url": "https://reliefweb.int/country/lby"}],
        "reliefweb_response_count": 24
    },
    {
        "region": "Venezuela",
        "country_code": "VE",
        "lat": 6.4238,
        "lon": -66.5897,
        "gdelt_sample_headlines": [
            "Economic pressures and political standoff drive continuing regional outward migration",
            "Public hospital medicine shortages reported in inland provincial capitals",
            "Humanitarian partners expand school feeding nutrition initiatives"
        ],
        "tone_range": (-5.6, -2.1),
        "event_volume_24h": 340,
        "event_volume_7d": 2250,
        "reliefweb_reports": [{"id": "rw-ve-01", "title": "Venezuela Humanitarian Response Update", "source": "UN OCHA", "format": "Situation Report", "url": "https://reliefweb.int/country/ven"}],
        "reliefweb_response_count": 32
    },
    {
        "region": "Colombia (Border Crisis)",
        "country_code": "CO",
        "lat": 4.5709,
        "lon": -74.2973,
        "gdelt_sample_headlines": [
            "Clashes between dissident factions displace communities in Cauca and Nariño",
            "Darien Gap transit corridor records high migrant flow amidst jungle perils",
            "Government peace negotiations face temporary suspension following regional attacks"
        ],
        "tone_range": (-5.4, -2.2),
        "event_volume_24h": 310,
        "event_volume_7d": 2050,
        "reliefweb_reports": [{"id": "rw-co-01", "title": "Colombia Humanitarian Needs Overview", "source": "UN OCHA", "format": "Situation Report", "url": "https://reliefweb.int/country/col"}],
        "reliefweb_response_count": 45
    },
    {
        "region": "Bangladesh (Cox's Bazar)",
        "country_code": "BD",
        "lat": 23.6850,
        "lon": 90.3563,
        "gdelt_sample_headlines": [
            "Cox's Bazar mega-camps face severe cyclone vulnerability and mudslides",
            "Funding cuts threaten essential monthly food ration allocations for 1 million refugees",
            "Armed gang violence reported in camps along Teknaf border corridor"
        ],
        "tone_range": (-5.9, -2.3),
        "event_volume_24h": 260,
        "event_volume_7d": 1780,
        "reliefweb_reports": [{"id": "rw-bd-01", "title": "Rohingya Refugee Joint Response Plan", "source": "ISCG", "format": "Appeal", "url": "https://reliefweb.int/country/bgd"}],
        "reliefweb_response_count": 52
    },
    {
        "region": "Papua New Guinea",
        "country_code": "PG",
        "lat": -6.314993,
        "lon": 143.95555,
        "gdelt_sample_headlines": [
            "Severe tribal violence escalates in Enga province leaving villages burned",
            "Massive landslide in Mulitaka isolates Highlands communities from road access",
            "Humanitarian relief convoys encounter security roadblocks along provincial highways"
        ],
        "tone_range": (-6.8, -2.8),
        "event_volume_24h": 140,
        "event_volume_7d": 890,
        "reliefweb_reports": [{"id": "rw-pg-01", "title": "PNG Emergency Response", "source": "UN OCHA", "format": "Situation Report", "url": "https://reliefweb.int/country/png"}],
        "reliefweb_response_count": 14
    },
    {
        "region": "Armenia / Azerbaijan (Border)",
        "country_code": "AM",
        "lat": 40.0691,
        "lon": 45.0382,
        "gdelt_sample_headlines": [
            "Diplomatic negotiations proceed on border delimitation agreements",
            "Integration programs assist over 100,000 displaced individuals from Karabakh",
            "Mine clearance operations continue in border agricultural sectors"
        ],
        "tone_range": (-4.2, -1.5),
        "event_volume_24h": 190,
        "event_volume_7d": 1350,
        "reliefweb_reports": [{"id": "rw-am-01", "title": "Armenia Refugee Response Plan", "source": "UNHCR", "format": "Appeal", "url": "https://reliefweb.int/country/arm"}],
        "reliefweb_response_count": 26
    }
]

