# Importing USLCI

These notebooks describe my journey trying to get USLCI to work with Brightway2. I created the notebooks in the following order:
* **1_My_little_database_bw2:** Here I tried to manually add a super tiny database `My little database` which consists on three unit processes interconnected. My goal here was to understand the data fields I need in Brightway2 to replicate the tiny dataset that I originally generated with OpenLCA.
* **2_My_little_database_JSON-LD_Import:** Here, I use the J
* **3_JSON-LD_Import-FY22_Q2_01_Zolca:** 

## Notes
The first notebook can run with the normal [brightway2 installation meta package](https://github.com/brightway-lca/brightway2). The other two notebooks run by installing the following packages individually (environment creation highly recommended!). All except bw2data and bw2io can be downloaded from its original source. If you want to test my JSON-LD importer (which I am currently debugging!) download bw2data and bw2io from my forked repositories. 
* [bw2data](https://github.com/macmribo/brightway2-data/tree/json_importer): Use branch json_importer. 
* [bw2calc](https://2.docs.brightway.dev/technical/bw2calc.html)
* [bw2io](https://github.com/macmribo/brightway2-io): Use branch json_importer.
* [bw_processing](https://github.com/brightway-lca/bw_processing)
* [bw_migrations](https://github.com/brightway-lca/bw_migrations)
