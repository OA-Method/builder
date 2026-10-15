// framework#251 / PR-Foundry/framework#275 — choose an inline-SVG block's icon from a
// searchable Lucide grid rather than by pasting SVG code.
import IconPicker from "@/components/Controls/IconPicker.vue";
import { __ } from "@/translation";
import blockController from "@/utils/blockController";

const isInlineSVG = () =>
	blockController.isBlockSelected() && Boolean(blockController.getFirstSelectedBlock()?.isInlineSVG());

export default {
	name: __("Icon"),
	properties: [
		{
			component: IconPicker,
			searchKeyWords: "Icon, SVG, Lucide, Symbol, Picker",
			condition: isInlineSVG,
		},
	],
	condition: isInlineSVG,
};
