# CCLAMP_Metadata
These scripts and documents were used to clean and enrich C-CLAMP's author metadata.
Please note that the scripts should be applied in the given order.

## Input
Most input files can be found in the `Data sources` folder. The scraped landing pages are stored in `DBNL scraped`.

## Steps
1. `C-CLAMP_metadata_cleanup_A.ipynb`: join all input files
2. Perform (semi-)manual cleanup in OpenRefine or similar tools and apply all changes specified in `Appendix B.pdf`
3. `C-CLAMP_metadata_cleanup_B.ipynb`: reformat and reconcile the different metadata fields after manual cleaning
4. `C-CLAMP_metadata_cleanup_C.ipynb`: add and correct values for country of birth and death by drawing information from the scraped landing pages
5. `C-CLAMP_metadata_hisclass.ipynb`: determine authors' social class based on their occupations
6. Add additional metadata by reloading the metadata file into OpenRefine and reconciling the author names with Wikidata (Optional)

## Ouptut
Intermediate saves can be found in the ´Intermediate files` folder.

The fully cleaned and enriched author metadata is saved as `author_metadata_hisclass_final.txt`.

For the results of the additional reconciliation step, please see `Reconciliation OpenRefine`.
