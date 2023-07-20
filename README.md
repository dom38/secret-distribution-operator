TODO:

- Figure out a way to abstract secret functions instead of writing the same functions for each provider
  - Reconciliation will be per provider type
  - Update will be per provider type, but a queue system can abstract this away
- Add logic to queue secret updates
- Add configurable queue workers to update secrets
- Refactor client singleton to return a dict of clients
- Initilise clients on startup
- Figure out how to actually check a secret has changed, timer won't catch all changes
