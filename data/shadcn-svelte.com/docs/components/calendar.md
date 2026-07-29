# Calendar

A calendar component that allows users to select dates.

[Docs](https://bits-ui.com/docs/components/calendar)

[API Reference](https://bits-ui.com/docs/components/calendar#api-reference)

### [Epicenter](https://github.com/EpicenterHQ/epicenter)

[Local-first, open source apps](https://github.com/EpicenterHQ/epicenter)

[Special Sponsor](https://github.com/EpicenterHQ/epicenter)

View Code

## [Blocks](calendar.md#blocks)

We have built a collection of 30+ calendar blocks that you can use to build your own calendar components.

See call calendar blocks in the [Blocks Library](../../blocks/calendar) page.

## [Installation](calendar.md#installation)

```bash
pnpm dlx shadcn-svelte@latest add calendar
```

```bash
npx shadcn-svelte@latest add calendar
```

```bash
bun x shadcn-svelte@latest add calendar
```

## [About](calendar.md#about)

The `<Calendar />` component is built on top of the [Bits UI Calendar](https://www.bits-ui.com/docs/components/calendar) component, which uses the [@internationalized/date](https://react-spectrum.adobe.com/internationalized/date/index.html) package to handle dates.

If you're looking for a range calendar, check out the [Range Calendar](range-calendar) component.

## [Date Picker](calendar.md#date-picker)

You can use the `<Calendar />` component to build a date picker. See the [Date Picker](date-picker) page for more information.

## [Examples](calendar.md#examples)

### [Range Calendar](calendar.md#range-calendar)

View Code

### [Month and Year Selector](calendar.md#month-and-year-selector)

View Code

### [Date of Birth Picker](calendar.md#date-of-birth-picker)

View Code

### [Date and Time Picker](calendar.md#date-and-time-picker)

View Code

### [Natural Language Picker](calendar.md#natural-language-picker)

This component uses the `chrono-node` library to parse natural language dates.

View Code

## [Upgrade Guide](calendar.md#upgrade-guide)

You can upgrade to the latest version of the `<Calendar />` component by running the following command:

```bash
pnpm dlx shadcn-svelte@latest add calendar
```

```bash
npx shadcn-svelte@latest add calendar
```

```bash
bun x shadcn-svelte@latest add calendar
```

When you're prompted to overwrite the existing files, select `Yes`. **If you have made any changes to the `Calendar` component, you will need to merge your changes with the new version.**

#### [Installing Blocks](calendar.md#installing-blocks)

After upgrading the `Calendar` component, you can add the new blocks with the following:

```bash
pnpm dlx shadcn-svelte@latest add calendar-02
```

```bash
npx shadcn-svelte@latest add calendar-02
```

```bash
bun x shadcn-svelte@latest add calendar-02
```

This will add the latest version of the calendar blocks.