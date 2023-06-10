// OAutho URL w/ identify and message.read scopes
// https://discord.com/oauth2/authorize?response_type=code&client_id=1117151974165577809&scope=identify%20messages.read&state=111&redirect_uri=https%3A%2F%2Fwww.cluna.co%2Flogin&prompt=consent
// https://discord.com/channels/1038097195422978059/1038097349660135474
const fs = require("fs");

const DISCORD_API_URL = "https://discord.com/api/v9";
const BEARER_TOKEN = "D2WaixpMXlq9vKgAUvkerIMueZOXjj";
const CHANNEL_ID = "1038097349660135474";

let messages = [];
async function getMessages(channelId, before) {
    if (messages.length >= 300) {
        return;
    }

    const url = `${DISCORD_API_URL}/channels/${channelId}/messages?limit=100${before ? `&before=${before}` : ""}`;
    console.log(url);
    const response = await fetch(url, {
        "headers": {
          "accept": "*/*",
          "accept-language": "en-US,en;q=0.9",
          "authorization": "MTExNzE2Nzc0NDIxNTk0MTE2MA.G38ry7.Pl2xMV-bLH4_L-DRUiuJWxoeRbA573CJtD8Wvw",
          "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
          "sec-ch-ua-mobile": "?0",
          "sec-ch-ua-platform": "\"macOS\"",
          "sec-fetch-dest": "empty",
          "sec-fetch-mode": "cors",
          "sec-fetch-site": "same-origin",
          "x-debug-options": "bugReporterEnabled",
          "x-discord-locale": "en-US",
          "x-discord-timezone": "America/Los_Angeles",
          "x-super-properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTQuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjExNC4wLjAuMCIsIm9zX3ZlcnNpb24iOiIxMC4xNS43IiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjIwNDIwNCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=",
          "cookie": "__dcfduid=cdaf89e007c111ee85b97d97667825a7; __sdcfduid=cdaf89e107c111ee85b97d97667825a77cf375b30b0afc4f83b47a10762f2af51d5aa1ee1d6be0d088046737100d039e; __cfruid=42a38098ed37d2382d1ff857035a85e08678f9a2-1686423945; locale=en-US; _gcl_au=1.1.332567564.1686423946; OptanonConsent=isIABGlobal=false&datestamp=Sat+Jun+10+2023+12%3A05%3A46+GMT-0700+(Pacific+Daylight+Time)&version=6.33.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1; _ga=GA1.1.101695491.1686423946; _ga_Q149DFWHT7=GS1.1.1686423946.1.1.1686424030.0.0.0; __cf_bm=quarptS82i.sT4HfPpqq64ZEkH0qFhp.XDcKhuPGXbo-1686426302-0-Ab0Pawl08uFBBxK4NYPbxUcuZfE1QZ84LKu7tp+NN0gpdJHex7BixkjCrNrZ4Q0EUQ==",
          "Referer": "https://discord.com/channels/1038097195422978059/1038097349660135474",
          "Referrer-Policy": "strict-origin-when-cross-origin"
        },
        "method": "GET"
      });
    const json = await response.json();
    // console.log(json.errors.limit);
    messages = [...messages, ...json];
    // console.log(messages[messages.length - 1]);
    await new Promise(resolve => setTimeout(resolve, Math.floor(Math.random() * 2000) + 4000));
    await getMessages(channelId, messages[messages.length - 1].id);
}

async function main() {
    await getMessages(CHANNEL_ID, 0);
    fs.writeFileSync("messages.json", JSON.stringify(messages));
    // const response = await fetch("https://discord.com/api/v9/channels/1038097349660135474/messages?limit=50", {
    // "headers": {
    //     "accept": "*/*",
    //     "accept-language": "en-US,en;q=0.9",
    //     "authorization": "MTExNzE2Nzc0NDIxNTk0MTE2MA.G38ry7.Pl2xMV-bLH4_L-DRUiuJWxoeRbA573CJtD8Wvw",
    //     "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    //     "sec-ch-ua-mobile": "?0",
    //     "sec-ch-ua-platform": "\"macOS\"",
    //     "sec-fetch-dest": "empty",
    //     "sec-fetch-mode": "cors",
    //     "sec-fetch-site": "same-origin",
    //     "x-debug-options": "bugReporterEnabled",
    //     "x-discord-locale": "en-US",
    //     "x-discord-timezone": "America/Los_Angeles",
    //     "x-super-properties": "eyJvcyI6Ik1hYyBPUyBYIiwiYnJvd3NlciI6IkNocm9tZSIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMTQuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjExNC4wLjAuMCIsIm9zX3ZlcnNpb24iOiIxMC4xNS43IiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjIwNDIwNCwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0=",
    //     "cookie": "__dcfduid=cdaf89e007c111ee85b97d97667825a7; __sdcfduid=cdaf89e107c111ee85b97d97667825a77cf375b30b0afc4f83b47a10762f2af51d5aa1ee1d6be0d088046737100d039e; __cfruid=42a38098ed37d2382d1ff857035a85e08678f9a2-1686423945; __cf_bm=yF.t3oZyOTn8MvtMlHf8fXfGyVLRlcHNOAnc1er4lBs-1686423946-0-AThvRV1/49sZmZzDsizYteyDHXKxrbTe/ndqpgpyeJXnwrmJXmKZmVYShajyBTO/jg==; locale=en-US; _gcl_au=1.1.332567564.1686423946; OptanonConsent=isIABGlobal=false&datestamp=Sat+Jun+10+2023+12%3A05%3A46+GMT-0700+(Pacific+Daylight+Time)&version=6.33.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1; _ga=GA1.1.101695491.1686423946; _ga_Q149DFWHT7=GS1.1.1686423946.1.1.1686424030.0.0.0",
    //     "Referer": "https://discord.com/channels/1038097195422978059/1038097349660135474",
    //     "Referrer-Policy": "strict-origin-when-cross-origin"
    // },
    // "body": null,
    // "method": "GET"
    // });
    // console.log(Object.keys(await response.json()));
}

main()
    .then(() => console.log("done"));

    