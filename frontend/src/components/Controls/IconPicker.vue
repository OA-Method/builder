<template>
	<div class="flex items-center justify-between gap-2">
		<InputLabel>{{ __("Icon") }}</InputLabel>
		<div class="flex items-center gap-2">
			<span
				class="flex size-7 items-center justify-center rounded border border-outline-gray-2 text-ink-gray-8 [&>svg]:size-4"
				v-html="currentSVG"></span>
			<Button size="sm" @click="open">{{ __("Choose icon") }}</Button>
		</div>
		<Dialog v-model="showDialog" :title="__('Choose an icon')" size="3xl">
			<template #default>
				<div class="flex flex-col gap-3">
					<BuilderInput
						type="text"
						:modelValue="query"
						@input="(val: string) => (query = val)"
						:placeholder="__('Search, e.g. heart, leaf, sun')"
						:autofocus="true" />
					<div v-if="!icons" class="p-6 text-center text-sm text-ink-gray-5">
						{{ loadError || __("Loading icons…") }}
					</div>
					<div v-else-if="!results.length" class="p-6 text-center text-sm text-ink-gray-5">
						{{ __("No icon matches that search.") }}
					</div>
					<div v-else class="grid max-h-[60vh] grid-cols-8 gap-1 overflow-y-auto">
						<button
							v-for="name in results"
							:key="name"
							:title="name"
							class="flex flex-col items-center gap-1 rounded p-2 text-ink-gray-8 hover:bg-surface-gray-2"
							@click="choose(name)">
							<span class="[&>svg]:size-6" v-html="svgFor(name)"></span>
							<span class="w-full truncate text-center text-[10px] text-ink-gray-5">{{ name }}</span>
						</button>
					</div>
					<p v-if="icons && matches.length > results.length" class="text-xs text-ink-gray-5">
						{{ __("Showing {0} of {1} — type to narrow the list.", [String(results.length), String(matches.length)]) }}
					</p>
				</div>
			</template>
		</Dialog>
	</div>
</template>

<script setup lang="ts">
// framework#251 / PR-Foundry/framework#275 — pick a Lucide icon for an inline-SVG block
// instead of pasting its code. Writes the same markup Lucide's own "Copy SVG" produces.
import InputLabel from "@/components/Controls/InputLabel.vue";
import { __ } from "@/translation";
import blockController from "@/utils/blockController";
import { Button, Dialog } from "frappe-ui";
import { computed, ref } from "vue";

type IconNode = [string, Record<string, string>][];

const MAX_RESULTS = 240;
const showDialog = ref(false);
const query = ref("");
const icons = ref<Record<string, IconNode> | null>(null);
const tags = ref<Record<string, string[]>>({});
const loadError = ref("");

const currentSVG = computed(() => (blockController.getInnerHTML() as string) || "");

// ~700 KB of icon data: a separate chunk, fetched the first time the picker opens.
const open = async () => {
	showDialog.value = true;
	if (icons.value) return;
	try {
		const [nodes, keywords] = await Promise.all([
			import("lucide-static/icon-nodes.json"),
			import("lucide-static/tags.json"),
		]);
		tags.value = keywords.default as Record<string, string[]>;
		icons.value = nodes.default as Record<string, IconNode>;
	} catch (e) {
		loadError.value = __("Could not load the icons.");
	}
};

const matches = computed(() => {
	if (!icons.value) return [];
	const words = query.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
	const names = Object.keys(icons.value);
	if (!words.length) return names;
	return names.filter((name) => {
		const haystack = [name, ...(tags.value[name] || [])].join(" ");
		return words.every((word) => haystack.includes(word));
	});
});
const results = computed(() => matches.value.slice(0, MAX_RESULTS));

const escape = (value: string) => String(value).replace(/&/g, "&amp;").replace(/"/g, "&quot;");

function svgFor(name: string, size = "24") {
	const children = (icons.value?.[name] || [])
		.map(([tag, attrs]) => {
			const pairs = Object.entries(attrs).map(([key, value]) => `${key}="${escape(value)}"`);
			return `<${tag} ${pairs.join(" ")} />`;
		})
		.join("");
	return (
		`<svg class="lucide lucide-${name}" xmlns="http://www.w3.org/2000/svg" width="${size}" ` +
		`height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" ` +
		`stroke-linecap="round" stroke-linejoin="round">${children}</svg>`
	);
}

// keep the size the block already had, so a swapped icon sits exactly where the old one did
function currentSize() {
	const match = currentSVG.value.match(/<svg[^>]*\swidth="(\d+(?:\.\d+)?)"/);
	return match ? match[1] : "24";
}

function choose(name: string) {
	blockController.setInnerHTML(svgFor(name, currentSize()));
	showDialog.value = false;
}
</script>
