# Date Picker

A date picker component with range and presets.

### [Epicenter](https://github.com/EpicenterHQ/epicenter)

[Local-first, open source apps](https://github.com/EpicenterHQ/epicenter)

[Special Sponsor](https://github.com/EpicenterHQ/epicenter)

View Code

## [Installation](date-picker.md#installation)

The Date Picker is built using a composition of the `<Popover />` and either the `<Calendar />` or `<RangeCalendar />` components.

See installations instructions for the [Popover](popover#installation), [Calendar](calendar#installation), and [Range Calendar](range-calendar#installation) components.

## [Usage](date-picker.md#usage)

lib/components/example-date-picker.svelte

```svelte
<script lang="ts">
  import CalendarIcon from "@lucide/svelte/icons/calendar";
  import {
    type DateValue,
    DateFormatter,
    getLocalTimeZone,
  } from "@internationalized/date";
  import { cn } from "$lib/utils.js";
  import { Button } from "$lib/components/ui/button/index.js";
  import { Calendar } from "$lib/components/ui/calendar/index.js";
  import * as Popover from "$lib/components/ui/popover/index.js";
  const df = new DateFormatter("en-US", {
    dateStyle: "long",
  });
  let value = $state<DateValue>();
</script>
<Popover.Root>
  <Popover.Trigger>
    {#snippet child({ props })}
      <Button
        variant="outline"
        class={cn(
          "w-[280px] justify-start text-start font-normal",
          !value && "text-muted-foreground"
        )}
        {...props}
      >
        <CalendarIcon class="me-2 size-4" />
        {value ? df.format(value.toDate(getLocalTimeZone())) : "Select a date"}
      </Button>
    {/snippet}
  </Popover.Trigger>
  <Popover.Content class="w-auto p-0">
    <Calendar bind:value type="single" initialFocus captionLayout="dropdown" />
  </Popover.Content>
</Popover.Root>
```

## [Examples](date-picker.md#examples)

### [Date of Birth Picker](date-picker.md#date-of-birth-picker)

View Code

### [Picker with Input](date-picker.md#picker-with-input)

View Code

### [Date and Time Picker](date-picker.md#date-and-time-picker)

View Code

### [Natural Language Picker](date-picker.md#natural-language-picker)

This component uses the `chrono-node` library to parse natural language dates.

View Code