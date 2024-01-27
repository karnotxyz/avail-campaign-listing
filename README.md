# Avail Clash of Nodes Listing

This is the official repo for the Karnot CLI and the Avail Clash of Nodes campaign. If you want your app chain
to be listed and ranked for the campaign, please create a PR on this repo which adds a JSON in the following
format to listing.json.

```json
{
  "name": "my_app_chain",
  "logo": "https://placehold.co/400x400",
  "rpc_url": "https://rpc.myappchain.xyz",
  "explorer_url": "https://explorer.myappchain.xyz",
  "metrics_endpoint": "https://metrics.myappchain.xyz",
  "id": "942ff35e-f048-4d10-ae61-6cb970cad2f0",
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
2. Create a PR with the name "✨ Adding <app_chain_name>"

Checkout this sample [PR](https://github.com/karnotxyz/avail-campaign-listing/pull/1).
