> The Karnot x Avail campaign has been paused until further notice. This means we won't be merging new PRs at the moment. However, if your PR has already been merged, you can continue to run your node. You can follow us [here](https://twitter.com/karnotxyz) to get future updates

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
  "id": "942ff35e-f048-4d10-ae61-6cb970cad2f0"
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
7. Make sure you're on the latest `main` version. If you're not, you should see an `Update branch` button on the PR page
8. If all your CI checks are passing, your branch should automatically merge.

Checkout this sample [PR](https://github.com/karnotxyz/avail-campaign-listing/pull/195).

## FAQs

### How to fix prettier?

Install npx and run `npx prettier@latest --write .` on the repo root.

### My `validate-entry` check keeps failing

Make sure all your entrypoints (`rpc_url`, `explorer_url`, `metrics_endpoint`) are up and working correctly.

### My `check-file-changes` check keeps failing

Make sure that you're only adding one file in your PR. This should be a .json file in the above mentioned
format and should be inside the `app_chains` folder.
