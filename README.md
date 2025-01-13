# visualize-protech-experience

These interactive visualizations aim to explore the growing presence of property technologies in residential spaces through a series of interactive visualizations. The data presented here is drawn from [Landlord Tech Watch survey](https://antievictionmappingproject.github.io/landlordtech/) responses, a crowdsourced survey that gathers tenant experiences with surveillance and management technologies in their buildings and neighborhoods.

All visualizations are created using D3.js in Observable Notebook, which you are welcome to fork and recreate following this link: [Anti-Evication Lab: Visualizing Protech Experience](https://observablehq.com/@anti-eviction-mapping-project/visualizing-protech-experience)

Dataset is built from Landlord Tech Watch survey response. Data Cleaning is done with Python locally. 
  - Zoomable Sunburst uses _sunburstHierachy.json_, which is built with _BuildSunburstHieracy.py_ on the survey responses data.
  - Bar Graph uses _technology_pairs_filtered.csv_, which is built with _TechPairs.py_ on the survey responses data.
  - Pie Charts uses _filtered technology_impact_covid_response.csv_, which is built with _Covidlmpact.py_ on the survey responses data.
  - _CleanTech.py_, _ExtractCompanyNames.py_, _ExtractNouns.py_ are helper classes for data cleaning. 
