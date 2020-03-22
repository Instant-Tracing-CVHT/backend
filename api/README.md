# weTrace serverless API

## Requirements

### Install `serverless` framework

    sudo npm install -g serverless

### `serverless-import-swagger` and other plugins

Within the project folder

    npm install

## Usage

### Obtain config files for env vars

Place `config.dev.yaml` within the `config/` folder

### Deploy stack

```bash
SLS_DEBUG=* serverless deploy --aws-profile=covid
```

NOTE: `covid` is my AWS profile in `~/aws/credentials` for the Hackathon

### Remove stack

```bash
serverless remove --aws-profile=covid
```
