# Todo

- [ ] [task-001](issues/task-001.md): a module for transducer-like operations
- [ ] [task-002](issues/task-002.md): monitor tools
- [ ] task-003: General Getter
- [ ] monitor/json_serializer should handle [namedtuples]
  - I may want to have a module for handling types

# GPT

- [Testing](/Users/carlos/code/journal/GPT_logs/2024/2024-11/2024-11-27-pytest.md)
- [Type Hints](./GPT_logs/2024/2024-10/2024-10-10-python-type-hints.md)
- [Iterator vs Generator](./GPT_logs/2024/2024-11/2024-11-18-py-iterator-vs-generator.md)
- [Exception Logging](./GPT_logs/2024/2024-11/2024-11-18-py-iterator-vs-generator.md)
- [Exception Logging](./GPT_logs/2025/2025-02/2025-02-05-py-exception-logging.md)
- [namedtuples](GPT_logs/2025/2025-03/2025-03-10-namedtuple-serialization.md)

# Structure

For a refactor I'm looking at

seqs, vecs
cols, maps

then the mixtures
  colseqs -> seqs of cols
  records -> seqs of maps
  rows    -> vecs of maps

or maybe I like rows instead of cols (no, `rows` implies a dict)
  seqs, vecs
  rows, maps
  records, vecmaps

colseqs -> seqs of cols
records -> seqs of maps
rows    -> vecs of maps


