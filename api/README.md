# weTrace serverless API

## Requirements

- `serverless` framework
- `serverless-import-swagger` plugin

## Usage

### Deploy stack

```bash
SLS_DEBUG=* serverless deploy --aws-profile=covid
```

NOTE: `covid` is my AWS profile in `~/aws/credentials` for the Hackathon

### Remove stack

```bash
serverless remove --aws-profile=covid
```
