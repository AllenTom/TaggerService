# TaggerService

Tagger image service for multiple model

## Installation

install pytorch cuda or cpu,version 2.1.0 and torchvision 0.16.0 are required

```shell
#cuda
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121
#cpu
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0
# install other dependencies
pip install -r requirements.txt
```

## Run

use uvicorn to run the service,more info see [uvicorn](https://www.uvicorn.org/)

```shell
python -m uvicorn main:app --reload 
```

## API

### tagger

url: `/tagger` [POST]

request body:

| key  | value | type | description |
|------|-------|------|-------------|
| file | file  | file | image file  |

url params:

| key       | value | type  | description           |
|-----------|-------|-------|-----------------------|
| model     | str   | str   | model                 |
| threshold | float | float | min confidence of tag |

model option:

- wd14_MOAT
- wd14_SwinV2
- wd14_ConvNext
- wd14_ConvNextV2
- wd14_ViT
- DeepDanbooru
- clip2

response:

```json
{
  "data": [
    {
      "tag": "Joong Keun Lee",
      "rank": 0.2200927734375
    },
    {
      "tag": "John Backderf",
      "rank": 0.2093505859375
    },
    {
      "tag": "keanu reeves",
      "rank": 0.275146484375
    },
    {
      "tag": "portrait of keanu reeves",
      "rank": 0.25732421875
    },
    {
      "tag": "portrait of john wick",
      "rank": 0.24658203125
    },
    {
      "tag": "keanu reeves as geralt of rivia",
      "rank": 0.234619140625
    },
    {
      "tag": "john wick",
      "rank": 0.23095703125
    }
  ],
  "error": null,
  "success": true
}
```

## state

url: `/state` [GET]

response:

```json
{
  "data": {
    "modelName": "clip2",
    "modelList": [
      "wd14_MOAT",
      "wd14_SwinV2",
      "wd14_ConvNext",
      "wd14_ConvNextV2",
      "wd14_ViT",
      "DeepDanbooru",
      "clip2"
    ]
  },
  "error": null,
  "success": true
}
```

## License

[MIT](LICENSE)