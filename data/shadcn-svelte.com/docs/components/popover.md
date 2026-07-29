# Popover

Displays rich content in a portal, triggered by a button.

[Docs](https://bits-ui.com/docs/components/popover)

[API Reference](https://bits-ui.com/docs/components/popover#api-reference)

### [Epicenter](https://github.com/EpicenterHQ/epicenter)

[Local-first, open source apps](https://github.com/EpicenterHQ/epicenter)

[Special Sponsor](https://github.com/EpicenterHQ/epicenter)

View Code

## [Installation](popover.md#installation)

```bash
pnpm dlx shadcn-svelte@latest add popover
```

```bash
npx shadcn-svelte@latest add popover
```

```bash
bun x shadcn-svelte@latest add popover
```

## [Usage](popover.md#usage)

```svelte
<script lang="ts">
  import * as Popover from "$lib/components/ui/popover/index.js";
</script>
```

```svelte
<Popover.Root>
  <Popover.Trigger>Open</Popover.Trigger>
  <Popover.Content>Place content for the popover here.</Popover.Content>
</Popover.Root>
```