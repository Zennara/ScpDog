# ScpDog
A watchdog and logger to Discord for hosting ScPrime servers. Designed to work on Linux servers. This is only capable of sending the logs from the commands `spc host` and `spc wallet`.

## Support
If you need help, or just want to chat or see my other projects, you can join my Discord by clicking [here](https://discord.gg/XcQSa9YaVx). If you want to donate, you can [here](https://www.paypal.me/keaganlandfried). Thanks :)

# Setting Up

## Download and Install
- Download the files and place them in any folder on your server. Ensure you have **root access**.
- Set up the proper permissions. These can be done with the following commands:
```
chmod 774 start.sh
chmod 774 install.sh
```
- Run the `install.sh` file. This will install `pip` and `discord.py` if you don't have them already.

## Configuration
- Open `config.json`
- `Discord_Webhook_URL` >> Enter your Discord webhook URL. You can find help [here](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).
- `ScPrime Install Path` >> Enter the path to your ScPrime server.
- `Auto Run Daily` >> Enter whether you want the file to run daily by itself. If not, you may want to schedule it with a [cron job](https://www.hostinger.com/tutorials/cron-job).
- `Display Wallet Information` >> Whether to display your wallet information from `spc wallet`.
- `Display Host Information` >> Whether to display your host information from `spc host`

Every other entry in the config file can be set to `true` or `false`. If you want the Discord alert to notify you for those statistics, set them to `true`. All entries follow structured indentation for categories and subvalues.
