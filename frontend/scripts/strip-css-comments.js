import { readFileSync, writeFileSync } from "fs";

const file = new URL("../../builder/public/reset.css", import.meta.url).pathname;
let css = readFileSync(file, "utf8")
	.replace(/\/\*![\s\S]*?\*\//g, "") // strip license comments
	.replace(/\n+/g, "") // collapse blank lines
	.trim();

// Put the whole reset in a cascade layer.
//
// webpage.html links this sheet AFTER Builder has already emitted the page's
// per-block styles, and both were unlayered — so the reset won on source order
// and silently overrode the client's own edits. That is the single cause behind
// a long tail of reported symptoms: flattened headings (Preflight sets
// `h1..h6 { font-size: inherit; font-weight: inherit }`), dead link colours
// (`a { color: inherit }`), compact CTAs, list bullets reappearing and lost
// paragraph spacing. Each had been answered individually with an unlayered
// counterweight in the site stylesheet, which then beat the client's edits in
// turn — moving the problem rather than removing it.
//
// A layer fixes the class: layered styles lose to every unlayered declaration
// regardless of specificity or order, so the reset still normalises anything
// nobody styles, while any per-block edit beats it by construction.
//
// @font-face is hoisted out so font loading is byte-for-byte what it was.
if (!css.includes("@layer builder-reset")) {
	const faces = [];
	const rest = [];
	let i = 0;
	for (;;) {
		const m = /@font-face\s*\{/g;
		m.lastIndex = i;
		const hit = m.exec(css);
		if (!hit) break;
		let depth = 1;
		let j = m.lastIndex;
		while (j < css.length && depth) {
			if (css[j] === "{") depth++;
			else if (css[j] === "}") depth--;
			j++;
		}
		rest.push(css.slice(i, hit.index));
		faces.push(css.slice(hit.index, j));
		i = j;
	}
	rest.push(css.slice(i));
	css = faces.join("") + "@layer builder-reset{" + rest.join("").trim() + "}";
}

writeFileSync(file, css);
