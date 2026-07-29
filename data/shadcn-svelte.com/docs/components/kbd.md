# Kbd

Used to display textual user input from keyboard.

### [Epicenter](https://github.com/EpicenterHQ/epicenter)

[Local-first, open source apps](https://github.com/EpicenterHQ/epicenter)

[Special Sponsor](https://github.com/EpicenterHQ/epicenter)

View Code

## [Installation](kbd.md#installation)

```bash
pnpm dlx shadcn-svelte@latest add kbd
```

```bash
npx shadcn-svelte@latest add kbd
```

```bash
bun x shadcn-svelte@latest add kbd
```

## [Usage](kbd.md#usage)

```svelte
<script lang="ts">
  import * as Kbd from "$lib/components/ui/kbd/index.js";
</script>
```

```svelte
<Kbd.Root>B</Kbd.Root>
```

## [Examples](kbd.md#examples)

### [Group](kbd.md#group)

Use the `Kbd.Group` component to group keyboard keys together.

View Code

### [Button](kbd.md#button)

Use the `Kbd.Root` component inside a `Button` component to display a keyboard key inside a button.

View Code

### [Tooltip](kbd.md#tooltip)

You can use the `Kbd.Root` component inside a `Tooltip` component to display a tooltip with a keyboard key.

View Code

### [Input Group](kbd.md#input-group)

You can use the `Kbd.Root` component inside a `InputGroup.Addon` component to display a keyboard key inside an input group.

View Code