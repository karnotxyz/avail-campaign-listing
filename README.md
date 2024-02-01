# Avail Clash of Nodes Listing

This is the official repo for the Karnot CLI and the Avail Clash of Nodes campaign. If you want your app chain
to be listed and ranked for the campaign, please create a PR on this repo which adds a JSON in the following
format to listing.json.

```json
{
  "name": "brknode",
  "logo": "https://https://i.imgur.com/5dc3wnP.png",
  "rpc_url": "http://129.151.196.70:9944",
  "explorer_url": "http://129.151.196.70:4000",
  "metrics_endpoint": "129.151.196.70:9615/metrics",
  "id": "8af34395-7b4c-4e67-b950-94dad41dd8a9"
}
```

## Details

1. `name`: The name of your app chain.
2. `logo`: A image link for the logo of your app chain
3. `rpc_url`: A public endpoint for your app chain to make RPC calls (port 9944 by default)
4. `explorer_url`: A public endpoint where your app chain explorer is visible
5. `metrics_endpoint`: A public endpoint for your prometheus metrics (port 9615 by default)

## PR instructions

1. Checkout from the main branch
2. Create a UUID. You can use an online [generator](https://www.uuidgenerator.net/).
3. Create a file with the name `<uuid>.json` inside the `app_chains` folder (`uuid` is the id generated in step 1).
4. Enter all the details mentioned above inside the JSON file.
5. Create a PR with the name "✨ Adding <app_chain_name>"
6. Wait for all CI checks to pass

Checkout this sample [PR](https://github.com/karnotxyz/avail-campaign-listing/pull/195).
