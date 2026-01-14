# Piper TTS Vast.ai PyWorker

PyWorker configuration for running Piper TTS on Vast.ai Serverless.

## Usage

This repo is designed to be used with Vast.ai's serverless bootstrap script:

1. Set `PYWORKER_REPO=https://github.com/DeepMakeLuke/piper-vastai-worker` in your template
2. Use the bootstrap script in your onstart-cmd

The PyWorker proxies requests from port 8000 to the Piper model server on port 18000.

## API

**POST /generate**
```json
{
  "text": "Hello world",
  "voice": "en_US-lessac-medium"
}
```

Returns base64-encoded raw audio.

**GET /health**
Returns `{"status": "ok"}`
