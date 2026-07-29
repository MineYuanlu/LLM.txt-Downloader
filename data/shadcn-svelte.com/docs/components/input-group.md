# Input Group

Display additional information or actions to an input or textarea.

### [Epicenter](https://github.com/EpicenterHQ/epicenter)

[Local-first, open source apps](https://github.com/EpicenterHQ/epicenter)

[Special Sponsor](https://github.com/EpicenterHQ/epicenter)

View Code

## [Installation](input-group.md#installation)

```bash
pnpm dlx shadcn-svelte@latest add input-group
```

```bash
npx shadcn-svelte@latest add input-group
```

```bash
bun x shadcn-svelte@latest add input-group
```

## [Usage](input-group.md#usage)

```svelte
<script lang="ts">
  import * as InputGroup from "$lib/components/ui/input-group/index.js";
  import SearchIcon from "@lucide/svelte/icons/search";
</script>
```

```svelte
<InputGroup.Root>
  <InputGroup.Input placeholder="Search..." />
  <InputGroup.Addon>
    <SearchIcon />
  </InputGroup.Addon>
  <InputGroup.Addon align="inline-end">
    <InputGroup.Button>Search</InputGroup.Button>
  </InputGroup.Addon>
</InputGroup.Root>
```

## [Examples](input-group.md#examples)

### [Icon](input-group.md#icon)

View Code

### [Text](input-group.md#text)

Display additional text information alongside inputs.

View Code

### [Button](input-group.md#button)

Add buttons to perform actions within the input group.

View Code

### [Tooltip](input-group.md#tooltip)

Add tooltips to provide additional context or help.

View Code

### [Textarea](input-group.md#textarea)

Input groups also work with textarea components. Use `block-start` or `block-end` for alignment.

View Code

### [Spinner](input-group.md#spinner)

Show loading indicators while processing input.

View Code

### [Label](input-group.md#label)

Add labels within input groups to improve accessibility.

View Code

### [Dropdown](input-group.md#dropdown)

Pair input groups with dropdown menus for complex interactions.

View Code

### [Button Group](input-group.md#button-group)

Wrap input groups with button groups to create prefixes and suffixes.

View Code

### [Custom Input](input-group.md#custom-input)

Add the `data-slot="input-group-control"` attribute to your custom input for automatic behavior and focus state handling.

No style is applied to the custom input. Apply your own styles using the `class` prop.

View Code