graph TD
  UserScript[User Python Script]
  FHIR[FHIR Server]
  UserScript -- GET Patient --> FHIR
  UserScript -- GET Observation --> FHIR
  FHIR -- Patient JSON --> UserScript
  FHIR -- Observation JSON --> UserScript
``` 