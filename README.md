# Electra Smart Integration With Home Assistant

![PyPI](https://img.shields.io/pypi/v/pyelectra?label=pypi%20package)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyelectra)

![alt text](https://brands.home-assistant.io/electrasmart/logo@2x.png)


Custom integrations to control [Electra Air](https://www.electra-air.co.il) devices with [Home Assistant](https://www.home-assistant.io)

Electra devices will be discovered after the `electrasmart` integration is configured

The configuration can be done via the frontend, the user must provide a valid phone number that registered with the [Electra Smart](https://www.electra-air.co.il/page/smart) app.

an OTP (One Time Password) will be generated and sent that phone number, provide this OTP in the config wizard and you should be good to go.

## Installation

1. Install the custom component in your HASS

    This can be done either through HACS:
    * `HACS`->`Integration`->`Custom repositories`
    * Enter `https://github.com/jafar-atili/home-assistant-electrasmart` 
    * click `Add`
    
    Manuall installation (without HACS)
    * Download the electrasmart directory and place it in `config/custom_components/`


2. Add `Electra Smart` Integration (`Configuration`->`Devices & Services`->`ADD INTEGRATION`) 
3. Enter your phone number (it must be registered with Electra Smart!)
4. Enter the one time password (received via SMS) 
5. Enjoy


## Debugging the integration

Add the following to your `configuration.yaml`

```
logger:
  default: info
  logs:
    custom_components.electrasmart: debug
    electra: debug
```

Share the logs with topic `[custom_components.electrasmart.climate]` and `[electra]`

 [In case you want to buy me a coffe :)](https://paypal.me/jafaratili?country.x=IL&locale.x=he_IL)
