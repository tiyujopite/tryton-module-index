# USAGE

## Build

All modules (Not recomended)

```bash
python api build
```

Some modules

```bash
python api build author/module author/module2
```

## Check

All modules (Not recomended)

```bash
python api check
```

Some modules

```bash
python api check author/module author/module2
```

## Build chunk

By default, the chunk is 50

```bash
python api build_chunk <chunk_index> <chunk_size:optional>

# Examples
python api build_chunk 0 # First 50
python api build_chunk 1 # From 51 to 100
python api build_chunk 0 100 # First 100
python api build_chunk 1 100 # From 101 to 200
```
