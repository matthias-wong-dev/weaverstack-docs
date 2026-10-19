(function (root, module) {
"use strict";
var FIELD = "", ROW = "", TABLE = "", LESS = "";
var KIND = {
TABLE: "Table", VIEW: "View", FOLDER: "Folder", SHORTCUT: "Shortcut",
TEST: "Test", ASSUMPTION: "Assumption", MODEL: "Semantic model", REPORT: "Report"
};
var CATALOGUE_ITEM = "Warehouse/_weaver";
var ITEM_TYPES = ["Lakehouse", "Warehouse", "SQLDatabase", "SemanticModel", "Report"];
var EDGE_KINDS = { D: "Dependency", S: "Shortcut", V: "Validation", E: "External" };
function parsePayload(text) {
var tables = {}, problems = [];
String(text || "").split(LESS).join("<").split(TABLE).forEach(function (chunk) {
if (!chunk) return;
var rows = chunk.split(ROW), head = rows[0].split(FIELD), name = head[0], cols = head.slice(1), out = [];
for (var r = 1; r < rows.length; r++) {
var fields = rows[r].split(FIELD);
if (fields.length !== cols.length) { problems.push(name + " row " + r + " has " + fields.length + " fields, not " + cols.length); continue; }
var row = {};
for (var c = 0; c < cols.length; c++) row[cols[c]] = fields[c] === "" ? null : fields[c];
out.push(row);
}
tables[name] = out;
});
return { tables: tables, problems: problems };
}
function num(value) {
if (value === null || value === undefined || value === "") return null;
var n = Number(value);
return isNaN(n) ? null : n;
}
function identityKey(item, schema, object) { return item + "|" + (schema || "") + "|" + (object || ""); }
function isValidation(node) { return node.kind === KIND.TEST || node.kind === KIND.ASSUMPTION; }
function itemType(label) { return String(label).split("/")[0]; }
function itemName(label) { var s = String(label); return s.slice(s.indexOf("/") + 1); }
function typeRank(type) { var i = ITEM_TYPES.indexOf(type); return i < 0 ? ITEM_TYPES.length : i; }
function compare(a, b) {
a = String(a === null || a === undefined ? "" : a).toLowerCase();
b = String(b === null || b === undefined ? "" : b).toLowerCase();
return a < b ? -1 : a > b ? 1 : 0;
}
function addTo(map, key, value) { var list = map.get(key); if (!list) map.set(key, list = []); list.push(value); }
/* The estate one payload describes: items, nodes with their current state,
the authoritative edges Health walks and the presentation edges the graph
draws, where a read through a shortcut is drawn from the shortcut. */
function buildModel(tables, problems) {
var t = function (name) { return tables[name] || []; };
var meta = t("meta")[0] || {}, page = t("page")[0] || {};
var m = {
page: page.name || "overview", at: num(meta.at) || Date.now(), tables: tables,
problems: (problems || []).slice(), items: new Map(), nodes: new Map(), byIdentity: new Map(),
internalItems: new Set(), edgeCount: 0, hiddenEdges: 0, externalCount: 0
};
t("internal").forEach(function (r) { m.internalItems.add(r.item); });
function item(label) {
var it = m.items.get(label);
if (!it) m.items.set(label, it = { label: label, type: itemType(label), name: itemName(label), workspace: null, target: null, version: null, nodes: [], internal: m.internalItems.has(label) || label === CATALOGUE_ITEM });
return it;
}
t("items").forEach(function (r) {
var it = item(r.item);
it.workspace = r.workspace; it.target = r.target; it.version = r.version;
});
var catalogue = m.items.get(CATALOGUE_ITEM);
m.catalogue = { name: catalogue ? catalogue.target : null, workspace: catalogue ? catalogue.workspace : null, version: catalogue ? catalogue.version : null };
t("nodes").forEach(function (r) {
if (m.nodes.has(r.key)) { m.problems.push("Two lineage nodes share the key " + r.key + "; one of them is not shown."); return; }
var flags = num(r.flags) || 0;
var n = {
key: r.key, item: r.item, schema: r.schema, object: r.object, kind: r.kind, label: r.label || r.object || r.item,
desc: r.description || "", canLoad: !!(flags & 1), isStatic: !!(flags & 2), isMirrored: !!(flags & 4), isInstalled: !!(flags & 8),
id: identityKey(r.item, r.schema, r.object), load: null, test: null, built: null,
up: [], down: [], vup: [], vdown: [], stubs: [], missing: [], kinds: {}
};
m.nodes.set(n.key, n);
m.byIdentity.set(n.id, n);
item(n.item).nodes.push(n);
});
var seen = new Set(), vseen = new Set(), edges = t("edges");
edges.forEach(function (r) {
var d = m.nodes.get(r.down), kind = EDGE_KINDS[r.kind] || r.kind;
if (!d) return;
if (kind === "External") { d.stubs.push(r.reference || r.up); m.externalCount += 1; return; }
var u = m.nodes.get(r.up);
if (!u) { if (r.reference) d.missing.push(r.reference); m.hiddenEdges += 1; return; }
var key = u.key + ">" + d.key;
if (!seen.has(key)) { seen.add(key); u.down.push(d.key); d.up.push(u.key); m.edgeCount += 1; }
var from = r.through && m.nodes.has(r.through) && r.through !== d.key ? m.nodes.get(r.through) : u;
var vkey = from.key + ">" + d.key;
if (!vseen.has(vkey)) {
vseen.add(vkey);
from.vdown.push(d.key); d.vup.push(from.key);
d.kinds[from.key] = from === u ? kind : "Dependency";
}
});
t("loads").forEach(function (r) {
var n = m.byIdentity.get(identityKey(r.item, r.schema, r.object));
if (n) n.load = status(r);
});
t("tests").forEach(function (r) {
var n = m.byIdentity.get(identityKey(r.item, r.schema, r.object));
if (n) { n.test = status(r); n.test.failures = num(r.failures); }
});
m.graphGaps = new Map();
t("built").forEach(function (r) {
var n = m.byIdentity.get(identityKey(r.item, r.schema, r.object));
if (n) n.built = num(r.built);
else if (!isInternal(m, r.item, r.schema)) m.graphGaps.set(r.item, (m.graphGaps.get(r.item) || 0) + 1);
});
m.items.forEach(function (it) {
it.nodes.sort(function (a, b) { return compare(a.schema, b.schema) || compare(a.label, b.label) || compare(a.key, b.key); });
});
m.workflows = t("workflows").map(function (r) {
return { id: r.workflow, started: num(r.started), completed: num(r.completed), records: num(r.records) || 0, failed: num(r.failed) || 0, tasks: r.tasks ? r.tasks.split(",") : [] };
});
m.workflows.sort(function (a, b) { return (b.completed || 0) - (a.completed || 0) || compare(a.id, b.id); });
m.workflowCount = num((t("workflowcount")[0] || {}).count);
return m;
}
function status(r) {
return { result: r.result, workflow: r.workflow, started: num(r.started), completed: num(r.completed), duration: num(r.duration) };
}
/* The catalogue, the Dashboard and the `_` surface the catalogue presents in
every item are Weaver's own; no page reports them as part of the estate. */
var INTERNAL_SCHEMA = /^(?:Files\/|Tables\/)?_$/;
function isInternal(m, item, schema) {
var it = m.items.get(item);
return !!(it && it.internal) || item === CATALOGUE_ITEM || INTERNAL_SCHEMA.test(schema || "");
}
function visibleItems(m) {
return Array.from(m.items.values()).filter(function (it) { return !it.internal; });
}
/* Shown names: a Lakehouse folder keeps its Files path. */
function qualified(node) {
if (!node.schema && !node.object) return node.item;
if (!node.object) return node.schema;
return node.schema + (String(node.schema).indexOf("Files") === 0 ? "/" : ".") + node.object;
}
var GREEN = "green", AMBER = "amber", RED = "red";
var SEVERITY_RANK = { green: 0, amber: 1, red: 2 };
var DEFAULT_AGE_MS = 24 * 3600 * 1000;
var LOAD_RED = ["Failed", "Error", "Blocked"];
var NO_DATA = ["Failed", "Error", "Blocked", "Pending"];
var ESTABLISHED = ["Succeeded", "Rejected", "Skipped"];
function isView(n) { return n.kind === KIND.VIEW; }
/* Observation, not execution: a loadable, a mirrored object and a View carry
load state. A View settles when its build succeeds. */
function participates(n) { return n.canLoad || n.isMirrored || isView(n); }
function isLoadSubject(n) { return (n.canLoad || n.isMirrored) && !isView(n); }
/* A mirrored object's state is recorded in the catalogue it mirrors, which
this Dashboard does not read. */
function effectiveLoad(n) { return n.isMirrored ? null : n.load; }
function establishedAt(n) {
var s = effectiveLoad(n);
return s && ESTABLISHED.indexOf(s.result) >= 0 ? s.completed : null;
}
/* Nodes in an order where every upstream comes first. */
function topological(m) {
var indegree = new Map(), order = [], queue = [];
m.nodes.forEach(function (n) { indegree.set(n.key, n.up.length); if (!n.up.length) queue.push(n.key); });
for (var i = 0; i < queue.length; i++) {
var n = m.nodes.get(queue[i]);
order.push(n);
n.down.forEach(function (d) { var k = indegree.get(d) - 1; indegree.set(d, k); if (k === 0) queue.push(d); });
}
if (order.length < m.nodes.size) {
var placed = new Set(order.map(function (n) { return n.key; }));
m.nodes.forEach(function (n) { if (!placed.has(n.key)) order.push(n); });
}
return order;
}
/* Over each node's lifecycle ancestors: whether one has not been processed,
the latest instant one was processed, and the latest it was processed or built. */
function ancestry(m) {
var out = new Map();
topological(m).forEach(function (n) {
var a = { unprocessed: false, latest: null, changed: null };
n.up.forEach(function (key) {
var p = m.nodes.get(key), pa = out.get(key) || { unprocessed: false, latest: null, changed: null };
if (pa.unprocessed) a.unprocessed = true;
a.latest = later(a.latest, pa.latest);
a.changed = later(a.changed, pa.changed);
if (participates(p)) {
var at = establishedAt(p);
if (at === null) a.unprocessed = true;
a.latest = later(a.latest, at);
a.changed = later(a.changed, later(at, p.built));
}
});
out.set(n.key, a);
});
return out;
}
function later(a, b) { return a === null ? b : b === null ? a : Math.max(a, b); }
function ancestorsOf(m, key) {
var seen = new Set(), stack = [key], out = [];
while (stack.length) {
m.nodes.get(stack.pop()).up.forEach(function (u) { if (!seen.has(u)) { seen.add(u); out.push(m.nodes.get(u)); stack.push(u); } });
}
return out;
}
function firstAncestor(m, key, test) {
var found = ancestorsOf(m, key).filter(function (a) { return participates(a) && test(a); });
found.sort(function (a, b) { return compare(a.id, b.id); });
return found[0] || null;
}
function finding(area, code, severity, node, result, message, s) {
return { area: area, code: code, severity: severity, node: node, result: result, message: message,
workflow: s ? s.workflow : null, completed: s ? s.completed : null, unobserved: false };
}
function assessHealth(m, options) {
options = options || {};
var asOf = options.asOf !== undefined ? options.asOf : m.at - DEFAULT_AGE_MS;
var anc = ancestry(m), load = [], tests = [], build = [], green = [];
var counts = { load: { subjects: 0 }, tests: { subjects: 0 }, build: { subjects: 0 } };
m.nodes.forEach(function (n) {
counts.build.subjects += 1;
if (isLoadSubject(n)) {
counts.load.subjects += 1;
var lf = loadFindings(m, n, anc, asOf), s = effectiveLoad(n);
load.push.apply(load, lf);
if (!lf.length) green.push(finding("load", "load_current", GREEN, n, s.result, "the last load " + s.result + (n.isStatic ? "; loaded once" : "; current with its dependencies"), s));
}
if (isValidation(n)) {
counts.tests.subjects += 1;
var tf = testFindings(m, n, anc);
tests.push.apply(tests, tf);
if (!tf.length) green.push(finding("tests", "test_current", GREEN, n, n.test.result, "the last run " + n.test.result + "; current with its dependencies", n.test));
if (!n.isInstalled) build.push(finding("build", "missing_validation_artefact", RED, n, null, "its definition or artefact is not installed; build the item again"));
else green.push(finding("build", "build_installed", GREEN, n, null, "installed and current"));
} else green.push(finding("build", "build_installed", GREEN, n, null, "installed and current"));
});
(m.tables.uncertified || []).forEach(function (r) {
if (!m.items.has(r.item) || m.items.get(r.item).internal || !m.items.get(r.item).target) return;
build.push({ area: "build", code: "not_installed", severity: RED, node: null, label: r.item + " " + r.schema + "." + r.object,
item: r.item, schema: r.schema, object: r.object,
result: null, message: "declared in the dictionary, but not certified in Registry", unobserved: false });
});
[load, tests, build].forEach(function (list) { list.sort(byFinding); });
return { asOf: asOf, at: m.at, load: load, tests: tests, build: build, counts: counts,
all: load.concat(tests, build).sort(byFinding), green: green.sort(byFinding) };
}
function byFinding(a, b) {
return SEVERITY_RANK[b.severity] - SEVERITY_RANK[a.severity] || compare(a.area, b.area) ||
compare(a.node ? a.node.id : a.label, b.node ? b.node.id : b.label) || compare(a.code, b.code);
}
function loadFindings(m, n, anc, asOf) {
var s = effectiveLoad(n), out = [];
if (!s || s.result === "Pending") {
var f = finding("load", "load_pending", AMBER, n, "Pending", n.isMirrored ?
"loaded in the catalogue this one mirrors, which the Dashboard does not read" :
"no load has processed this object since it was built", s);
f.unobserved = n.isMirrored;
return [f];
}
if (LOAD_RED.indexOf(s.result) >= 0) return [finding("load", "load_failed", RED, n, s.result, "the last load " + s.result, s)];
if (s.result === "Rejected") out.push(finding("load", "load_rejected", AMBER, n, s.result, "the last load completed with rejected rows", s));
if (NO_DATA.indexOf(s.result) >= 0 || n.isStatic) return out;
if (s.completed !== null && s.completed < asOf) out.push(finding("load", "load_stale_time", AMBER, n, s.result, "last loaded " + stamp(s.completed), s));
var a = anc.get(n.key);
if (a.unprocessed) {
var behind = firstAncestor(m, n.key, function (p) { return establishedAt(p) === null; });
out.push(finding("load", "load_ancestor_unestablished", AMBER, n, s.result,
(behind ? behind.label : "an upstream object") + " has not been processed since it was built", s));
}
var loaded = establishedAt(n);
if (loaded !== null && a.latest !== null && a.latest > loaded) {
var newer = firstAncestor(m, n.key, function (p) { var at = establishedAt(p); return at !== null && at > loaded; });
out.push(finding("load", "load_stale_ancestor", AMBER, n, s.result,
(newer ? newer.label : "an upstream object") + " has been established since this object was loaded", s));
}
return out;
}
function testFindings(m, n, anc) {
var s = n.test;
if (!s) return [finding("tests", "test_pending", AMBER, n, "Pending", "this validation has not run since it was built")];
if (LOAD_RED.indexOf(s.result) >= 0) return [finding("tests", "test_failed", RED, n, s.result, "the last run " + s.result, s)];
if (s.result !== "Succeeded") return [finding("tests", "test_pending", AMBER, n, s.result, "the last run " + s.result, s)];
var at = s.completed, a = anc.get(n.key);
if (at === null || a.changed === null || a.changed <= at) return [];
var moved = firstAncestor(m, n.key, function (p) { return (establishedAt(p) || at) > at || (p.built || at) > at; });
var how = moved && (establishedAt(moved) || at) > at ? "loaded" : "built";
return [finding("tests", "test_stale_dependency", AMBER, n, s.result,
(moved ? moved.label : "an upstream object") + " has been " + how + " since this validation passed", s)];
}
function worstOf(list) {
return list.reduce(function (w, f) { return SEVERITY_RANK[f.severity] > SEVERITY_RANK[w] ? f.severity : w; }, GREEN);
}
/* ---- readiness: derived from recorded dependencies, never a queue -------- */
/* The nearest upstream objects that carry load state, walking through those
that do not, such as a shortcut. */
function nearestStateful(m, n) {
var seen = new Set(), stack = n.up.slice(), out = [];
while (stack.length) {
var key = stack.pop();
if (seen.has(key)) continue;
seen.add(key);
var p = m.nodes.get(key);
if (participates(p)) out.push(p);
else stack.push.apply(stack, p.up);
}
return out.sort(function (a, b) { return compare(a.label, b.label); });
}
var READINESS = { CURRENT: "Current", READY: "Ready", WAITING: "Waiting", ELSEWHERE: "Loaded elsewhere", NONE: "Not loaded here" };
/* Readiness keeps apart what happened (the outcome) and whether the recorded
dependencies would let it run again now. */
function readiness(m, n) {
if (n.isMirrored) return { state: READINESS.ELSEWHERE, waitingOn: [], unprocessed: 0 };
if (!n.canLoad) return { state: READINESS.NONE, waitingOn: [], unprocessed: 0 };
var ups = nearestStateful(m, n), waiting = ups.filter(function (p) { return establishedAt(p) === null; });
if (waiting.length) return { state: READINESS.WAITING, waitingOn: waiting, unprocessed: waiting.length };
var loaded = establishedAt(n);
var behind = loaded === null || ups.some(function (p) { return establishedAt(p) > loaded; });
return { state: behind ? READINESS.READY : READINESS.CURRENT, waitingOn: [], unprocessed: 0 };
}
function tone(result) {
switch (result) {
case "Succeeded": case "Skipped": return "ok";
case "Failed": case "Error": case "Blocked": return "bad";
case "Rejected": return "warn";
case "Pending": return "wait";
default: return "none";
}
}
/* A node sits mid-column with its label, at most LABEL wide, centred beneath
it; a selection's columns leave room either side of a label for its
expansion markers. */
var GEOMETRY = { COL: 290, SUB: 260, ROW: 40, HEAD: 54, PAD: 22, GAP: 40, LABEL: 200 };
var WINDOW_GEOMETRY = { COL: 390, SUB: 360, ROW: 58, HEAD: 54, PAD: 22, GAP: 48, LABEL: 240 };
var BUDGET = { NODES: 600, EDGES: 3000, REVEAL: 40, EXPANDED: 600 };
function itemLevels(m, items) {
var ups = new Map(), level = new Map(), visiting = new Set();
items.forEach(function (it) { ups.set(it.label, new Set()); });
m.nodes.forEach(function (n) {
n.vup.forEach(function (u) {
var from = m.nodes.get(u).item;
if (from !== n.item && ups.has(n.item) && ups.has(from)) ups.get(n.item).add(from);
});
});
function visit(label) {
if (level.has(label)) return level.get(label);
if (visiting.has(label)) return -1;
visiting.add(label);
var deepest = -1;
Array.from(ups.get(label)).sort(compare).forEach(function (u) { deepest = Math.max(deepest, visit(u)); });
visiting.delete(label);
level.set(label, deepest + 1);
return deepest + 1;
}
items.forEach(function (it) { visit(it.label); });
return level;
}
/* Layers inside one item: longest path to a sink over the item's own edges. */
function itemLayers(m, it) {
var shortcuts = [], validations = [], ranked = [], inItem = new Set();
it.nodes.forEach(function (n) {
if (n.kind === KIND.SHORTCUT) shortcuts.push(n);
else if (isValidation(n)) validations.push(n);
else { ranked.push(n); inItem.add(n.key); }
});
var out = new Map(), indegree = new Map(), order = [], ordered = new Set(), queue = [];
ranked.forEach(function (n) {
indegree.set(n.key, n.vup.filter(function (u) { return inItem.has(u); }).length);
});
ranked.forEach(function (n) { if (!indegree.get(n.key)) queue.push(n.key); });
for (var i = 0; i < queue.length; i++) {
order.push(queue[i]);
ordered.add(queue[i]);
m.nodes.get(queue[i]).vdown.forEach(function (d) {
if (!inItem.has(d)) return;
var k = indegree.get(d) - 1;
indegree.set(d, k);
if (k === 0) queue.push(d);
});
}
ranked.forEach(function (n) { if (!ordered.has(n.key)) order.push(n.key); });
var toSink = new Map();
for (var j = order.length - 1; j >= 0; j--) {
var key = order[j], best = 0;
m.nodes.get(key).vdown.forEach(function (d) { if (toSink.has(d)) best = Math.max(best, toSink.get(d) + 1); });
toSink.set(key, best);
}
var depth = 0;
toSink.forEach(function (v) { depth = Math.max(depth, v); });
var offset = shortcuts.length ? 1 : 0;
ranked.forEach(function (n) { out.set(n.key, offset + depth - toSink.get(n.key)); });
shortcuts.forEach(function (n) { out.set(n.key, 0); });
var last = (ranked.length ? depth + offset : offset - 1) + 1;
validations.forEach(function (n) { out.set(n.key, last); });
return { layer: out, shortcuts: shortcuts.length > 0, validations: validations.length > 0, last: last };
}
/* Row order inside each layer: alphabetical, then barycentre sweeps over the
item's own edges so that related nodes sit near one another. */
function orderLayers(m, it, layers) {
var byLayer = [];
it.nodes.forEach(function (n) {
var l = layers.layer.get(n.key);
(byLayer[l] = byLayer[l] || []).push(n);
});
for (var l = 0; l < byLayer.length; l++) byLayer[l] = byLayer[l] || [];
var index = new Map();
function renumber(list) { list.forEach(function (n, i) { index.set(n.key, i / Math.max(1, list.length - 1)); }); }
byLayer.forEach(renumber);
function sweep(list, neighbours) {
var bary = new Map();
list.forEach(function (n) {
var near = neighbours(n).filter(function (k) { return index.has(k) && m.nodes.get(k).item === it.label; });
bary.set(n.key, near.length ? near.reduce(function (s, k) { return s + index.get(k); }, 0) / near.length : index.get(n.key));
});
list.sort(function (a, b) { return bary.get(a.key) - bary.get(b.key) || compare(a.schema, b.schema) || compare(a.label, b.label) || compare(a.key, b.key); });
renumber(list);
}
for (var pass = 0; pass < 3; pass++) {
for (var f = 1; f < byLayer.length; f++) sweep(byLayer[f], function (n) { return n.vup; });
for (var b = byLayer.length - 2; b >= 0; b--) sweep(byLayer[b], function (n) { return n.vdown; });
}
return byLayer;
}
function layoutEstate(m, geometry) {
var items = visibleItems(m).filter(function (it) { return it.nodes.length; });
var levels = itemLevels(m, items);
items.sort(function (a, b) {
return levels.get(a.label) - levels.get(b.label) || typeRank(a.type) - typeRank(b.type) || compare(a.name, b.name);
});
var G = geometry || GEOMETRY, pos = new Map(), bands = [];
items.forEach(function (it) {
var layers = itemLayers(m, it), byLayer = orderLayers(m, it, layers);
var maxRows = Math.max(40, Math.ceil(Math.sqrt(it.nodes.length) * 5));
var x = 0, rows = 1, columns = [], drawn = 0;
byLayer.forEach(function (list, l) {
var subs = Math.max(1, Math.ceil(list.length / maxRows)), perSub = Math.max(1, Math.ceil(list.length / subs));
var width = subs > 1 ? subs * G.SUB : G.COL;
columns.push({ layer: l, x: x, width: width, count: list.length,
kind: layers.shortcuts && l === 0 ? "shortcuts" : layers.validations && l === layers.last ? "validations" : "objects" });
list.forEach(function (n, i) {
var sub = Math.floor(i / perSub), row = i - sub * perSub;
pos.set(n.key, { x: x + (subs > 1 ? sub * G.SUB + G.SUB / 2 : G.COL / 2), y: row + ((drawn + sub) % 2) / 2, layer: l });
});
drawn += subs;
rows = Math.max(rows, Math.min(list.length, perSub) + (drawn > 1 ? 0.5 : 0));
x += width;
});
bands.push({ item: it, width: G.PAD * 2 + x, height: G.HEAD + rows * G.ROW + G.PAD, columns: columns, level: levels.get(it.label) });
});
var byLevel = [];
bands.forEach(function (b) { (byLevel[b.level] = byLevel[b.level] || []).push(b); });
var cx = 0, width = 0, height = 0, centre = new Map();
byLevel.forEach(function (column) {
if (!column) return;
column.forEach(function (b) {
var ups = [];
b.item.nodes.forEach(function (n) {
n.vup.forEach(function (u) { var c = centre.get(m.nodes.get(u).item); if (c !== undefined) ups.push(c); });
});
b.order = ups.length ? ups.reduce(function (a, v) { return a + v; }, 0) / ups.length : Infinity;
});
column.sort(function (a, b) {
return (a.order - b.order) || typeRank(a.item.type) - typeRank(b.item.type) || compare(a.item.name, b.item.name);
});
var cy = 0, columnWidth = 0;
column.forEach(function (b) {
b.x = cx; b.y = cy;
centre.set(b.item.label, cy + b.height / 2);
cy += b.height + G.GAP;
columnWidth = Math.max(columnWidth, b.width);
});
height = Math.max(height, cy - G.GAP);
cx += columnWidth + G.GAP * 3;
width = cx - G.GAP * 3;
});
bands.forEach(function (b) {
b.item.nodes.forEach(function (n) {
var p = pos.get(n.key);
p.x = b.x + G.PAD + p.x;
p.y = b.y + G.HEAD + p.y * G.ROW + G.ROW / 2 - 8;
p.band = b;
});
b.columns.forEach(function (c) { c.x += b.x + G.PAD; });
});
return { bands: bands, pos: pos, width: width, height: height, geometry: G };
}
/* The estate restricted to keys: the same items and nodes, with neighbour lists
cut to the subset, for layoutEstate. Each item remembers its full size. */
function subModel(m, keys) {
var nodes = new Map(), items = new Map();
keys.forEach(function (k) {
var n = m.nodes.get(k), c = Object.create(n);
c.vup = n.vup.filter(function (j) { return keys.has(j); });
c.vdown = n.vdown.filter(function (j) { return keys.has(j); });
nodes.set(k, c);
});
m.items.forEach(function (it, label) {
var own = it.nodes.filter(function (n) { return keys.has(n.key); });
if (!own.length) return;
var c = Object.create(it);
c.nodes = own.map(function (n) { return nodes.get(n.key); });
c.total = it.nodes.length;
items.set(label, c);
});
return { nodes: nodes, items: items };
}
/* ---- the window around a selection --------------------------------------- */
/* The selected nodes and their lineage to the requested depths, nearest first
up to the budget, plus whatever the reader has expanded. Every neighbour left
out is counted on the shown node it hangs from, as a marker that expands it.
Given within, the lineage stays inside it, and with nothing selected the
window is all of it. */
function focusWindow(m, selection, upDepth, downDepth, expanded, within) {
var seeds = (Array.isArray(selection) ? selection : [selection]).filter(function (k) { return m.nodes.has(k) && (!within || within.has(k)); });
if (!seeds.length && !within) return null;
var focus = seeds.length ? seeds[seeds.length - 1] : null, dist = new Map();
seeds.forEach(function (k) { dist.set(k, 0); });
function walk(next, sign, depth) {
var limit = depth < 0 ? Infinity : depth, frontier = seeds.slice();
for (var step = 1; step <= limit && frontier.length; step++) {
var found = [];
frontier.forEach(function (k) {
next(m.nodes.get(k)).forEach(function (j) { if (!dist.has(j) && (!within || within.has(j))) { dist.set(j, sign * step); found.push(j); } });
});
frontier = found;
}
}
walk(function (n) { return n.vup; }, -1, upDepth);
walk(function (n) { return n.vdown; }, 1, downDepth);
var ranked = Array.from(dist, function (e) { return { key: e[0], dist: e[1] }; });
ranked.sort(function (a, b) {
return Math.abs(a.dist) - Math.abs(b.dist) || (a.dist > 0) - (b.dist > 0) ||
compare(m.nodes.get(a.key).label, m.nodes.get(b.key).label) || compare(a.key, b.key);
});
var lineage = new Map();
if (seeds.length) ranked.slice(0, BUDGET.NODES).forEach(function (r) { lineage.set(r.key, r.dist); });
else within.forEach(function (k) { if (m.nodes.has(k)) lineage.set(k, 0); });
var shown = new Set(lineage.keys()), added = new Set();
(expanded || []).forEach(function (k) {
if (m.nodes.has(k) && !shown.has(k) && added.size < BUDGET.EXPANDED) { shown.add(k); added.add(k); }
});
var edges = [], plain = [];
shown.forEach(function (d) {
m.nodes.get(d).vup.forEach(function (u) {
if (!shown.has(u)) return;
var du = lineage.get(u), dd = lineage.get(d);
var line = du !== undefined && dd !== undefined && ((dd <= 0 && du < 0 && du < dd) || (du >= 0 && dd > 0 && dd > du));
(line ? edges : plain).push({ u: u, d: d, side: line ? (dd <= 0 ? "up" : "down") : null });
});
});
var edgeTotal = edges.length + plain.length;
edges = edges.concat(plain).slice(0, BUDGET.EDGES);
var more = new Map(), hidden = new Set();
shown.forEach(function (k) {
var n = m.nodes.get(k);
var up = n.vup.filter(function (j) { return !shown.has(j); }), down = n.vdown.filter(function (j) { return !shown.has(j); });
up.concat(down).forEach(function (j) { hidden.add(j); });
if (up.length || down.length) more.set(k, { up: up, down: down });
});
return { focus: focus, seeds: new Set(seeds), lineage: lineage, expanded: added, shown: shown, edges: edges, more: more,
hidden: hidden.size, reach: dist.size, truncated: seeds.length > 0 && dist.size > lineage.size, edgesDropped: edgeTotal - edges.length };
}
/* The neighbours a marker expands, nearest names first. */
function revealFrom(m, keys) {
return keys.slice().sort(function (a, b) { return compare(m.nodes.get(a).label, m.nodes.get(b).label) || compare(a, b); }).slice(0, BUDGET.REVEAL);
}
var CELL = 64, LABEL_DROP = 20;
function GraphView(host, m, lay, options) {
var self = this;
this.m = m; this.lay = lay; this.o = options; this.s = options.state;
this.host = host;
this.canvas = el("canvas", { "class": "wd-graph-canvas", tabindex: "0", role: "img", "aria-label": options.label || "Lineage graph" });
this.tip = el("div", { "class": "wd-tip", hidden: "hidden" });
this.hint = el("div", { "class": "wd-hint", hidden: "hidden", text: "Hold Ctrl or ⌘ and scroll to zoom" });
host.appendChild(this.canvas); host.appendChild(this.tip); host.appendChild(this.hint);
this.index(lay);
this.markers = [];
this.win = null;
this.hover = null;
this.bind();
if (root.ResizeObserver) new root.ResizeObserver(function () { self.resize(); }).observe(host);
else root.addEventListener("resize", function () { self.resize(); });
this.resize();
}
/* A spatial index of the layout's nodes, for hit testing. */
GraphView.prototype.index = function (lay) {
var grid = new Map();
lay.pos.forEach(function (p, key) {
var cell = Math.floor(p.x / CELL) + "|" + Math.floor(p.y / CELL);
var list = grid.get(cell);
if (!list) grid.set(cell, list = []);
list.push(key);
});
this.lay = lay; this.grid = grid;
};
GraphView.prototype.resize = function () {
var box = this.host.getBoundingClientRect();
this.width = Math.max(1, box.width); this.height = Math.max(1, box.height);
var ratio = canvasRatio(this.width, this.height);
this.canvas.width = Math.round(this.width * ratio); this.canvas.height = Math.round(this.height * ratio);
this.canvas.style.width = this.width + "px"; this.canvas.style.height = this.height + "px";
this.ratio = ratio;
if (!this.s.view) this.fitAll(false);
this.draw();
};
GraphView.prototype.palette = function () {
var cs = root.getComputedStyle(this.host), v = function (name) { return cs.getPropertyValue(name).trim(); };
var P = {};
["ink", "ink-soft", "muted", "faint", "line", "line-strong", "surface", "paper", "paper-deep", "blue", "blue-dark", "blue-soft",
"green", "green-soft", "amber", "amber-soft", "red", "red-soft", "violet", "violet-soft", "up", "down", "band", "band-line", "sans", "mono"]
.forEach(function (name) { P[name] = v("--" + name); });
return P;
};
function kindColour(kind, P) {
switch (kind) {
case KIND.FOLDER: return P.green;
case KIND.SHORTCUT: return P.amber;
case KIND.TEST: case KIND.ASSUMPTION: return P.violet;
case KIND.MODEL: case KIND.REPORT: return P["blue-dark"];
default: return P.blue;
}
}
function toneColour(t, P) {
return { ok: P.green, bad: P.red, warn: P.amber, wait: P.amber, none: P.faint }[t] || P.faint;
}
/* One glyph per kind, about 12 px across. */
function glyph(ctx, kind, x, y, colour, P) {
ctx.lineWidth = 1.6;
ctx.strokeStyle = colour; ctx.fillStyle = colour;
ctx.beginPath();
switch (kind) {
case KIND.TABLE: ctx.arc(x, y, 5, 0, 7); ctx.fill(); break;
case KIND.VIEW:
ctx.fillStyle = P.surface; ctx.arc(x, y, 5, 0, 7); ctx.fill(); ctx.stroke();
ctx.beginPath(); ctx.fillStyle = colour; ctx.arc(x, y, 1.8, 0, 7); ctx.fill(); break;
case KIND.FOLDER:
ctx.moveTo(x - 6, y - 4); ctx.lineTo(x - 2, y - 4); ctx.lineTo(x - 0.5, y - 2.5); ctx.lineTo(x + 6, y - 2.5);
ctx.lineTo(x + 6, y + 4.5); ctx.lineTo(x - 6, y + 4.5); ctx.closePath(); ctx.fill(); break;
case KIND.SHORTCUT:
ctx.fillStyle = P.surface; ctx.moveTo(x, y - 6); ctx.lineTo(x + 6, y); ctx.lineTo(x, y + 6); ctx.lineTo(x - 6, y); ctx.closePath();
ctx.fill(); ctx.stroke(); break;
case KIND.TEST: ctx.moveTo(x, y - 6); ctx.lineTo(x + 6, y + 4.5); ctx.lineTo(x - 6, y + 4.5); ctx.closePath(); ctx.fill(); break;
case KIND.ASSUMPTION:
ctx.fillStyle = P.surface; ctx.moveTo(x, y - 6); ctx.lineTo(x + 6, y + 4.5); ctx.lineTo(x - 6, y + 4.5); ctx.closePath();
ctx.fill(); ctx.stroke(); break;
case KIND.MODEL:
for (var i = 0; i < 6; i++) { var a = Math.PI / 3 * i + Math.PI / 6; ctx[i ? "lineTo" : "moveTo"](x + 6 * Math.cos(a), y + 6 * Math.sin(a)); }
ctx.closePath(); ctx.fill(); break;
case KIND.REPORT:
ctx.fillStyle = P.surface; ctx.rect(x - 5.5, y - 5.5, 11, 11); ctx.fill(); ctx.stroke();
ctx.beginPath(); ctx.fillStyle = colour; ctx.rect(x - 3, y, 1.6, 3); ctx.rect(x - 0.8, y - 3, 1.6, 6); ctx.rect(x + 1.4, y - 1.5, 1.6, 4.5); ctx.fill(); break;
default: ctx.fillStyle = P.surface; ctx.arc(x, y, 4.5, 0, 7); ctx.fill(); ctx.stroke();
}
}
function curve(ctx, a, b) {
var x1 = a.x + 7, y1 = a.y, x2 = b.x - 8, y2 = b.y, c = Math.max(36, Math.abs(x2 - x1) * 0.45);
ctx.moveTo(x1, y1);
ctx.bezierCurveTo(x1 + c, y1, x2 - c, y2, x2, y2);
}
function arrow(ctx, b) {
ctx.moveTo(b.x - 7, b.y); ctx.lineTo(b.x - 12, b.y - 3); ctx.lineTo(b.x - 12, b.y + 3); ctx.closePath();
}
/* Whether the viewport shows the node, or with no node any part of the estate. */
GraphView.prototype.showing = function (key) {
var r = this.visibleRect(), p = key ? this.lay.pos.get(key) : null;
if (p) return p.x > r.x && p.x < r.x + r.w && p.y > r.y && p.y < r.y + r.h;
return r.x < this.lay.width && r.x + r.w > 0 && r.y < this.lay.height && r.y + r.h > 0;
};
/* Show a window over its own layout, or with no window the whole estate. */
GraphView.prototype.setWindow = function (win, lay) { this.win = win; this.index(lay); this.draw(); };
GraphView.prototype.visibleRect = function () {
var v = this.s.view;
return { x: -v.x / v.k, y: -v.y / v.k, w: this.width / v.k, h: this.height / v.k };
};
GraphView.prototype.draw = function () {
var self = this;
if (this.pending) return;
this.pending = true;
(root.requestAnimationFrame || function (f) { return setTimeout(f, 16); })(function () { self.pending = false; self.paint(); });
};
GraphView.prototype.paint = function () {
var ctx = this.canvas.getContext("2d"), P = this.palette(), v = this.s.view, m = this.m, lay = this.lay, win = this.win;
var mode = this.o.mode || "kind", self = this;
ctx.setTransform(this.ratio, 0, 0, this.ratio, 0, 0);
ctx.clearRect(0, 0, this.width, this.height);
ctx.translate(v.x, v.y); ctx.scale(v.k, v.k);
var r = this.visibleRect(), pad = 240;
function inView(x, y) { return x > r.x - pad && x < r.x + r.w + pad && y > r.y - 40 && y < r.y + r.h + 40; }
var k = v.k, labels = k >= 0.5, sans = P.sans || "sans-serif", mono = P.mono || "monospace";
lay.bands.forEach(function (b) {
if (b.x > r.x + r.w || b.x + b.width < r.x || b.y > r.y + r.h || b.y + b.height < r.y) return;
ctx.beginPath(); roundRect(ctx, b.x, b.y, b.width, b.height, 12);
ctx.fillStyle = P.band; ctx.fill(); ctx.lineWidth = 1 / k; ctx.strokeStyle = P["band-line"]; ctx.stroke();
b.columns.forEach(function (c) {
if (c.kind === "objects") return;
ctx.beginPath(); roundRect(ctx, c.x - 12, b.y + lay.geometry.HEAD - 13, c.width - 6, b.height - lay.geometry.HEAD + 5, 9);
ctx.fillStyle = c.kind === "shortcuts" ? P["amber-soft"] : P["violet-soft"]; ctx.fill();
if (k > 0.45) {
ctx.fillStyle = c.kind === "shortcuts" ? P.amber : P.violet;
ctx.font = "700 9px " + mono;
ctx.fillText(c.kind === "shortcuts" ? "SHORTCUTS" : "TESTS", c.x - 4, b.y + lay.geometry.HEAD - 2);
}
});
var grow = Math.max(1, 0.9 / k), eyebrow = 9.5 * grow, name = Math.min(13 * grow, b.width / 7);
ctx.fillStyle = P.blue; ctx.font = "700 " + eyebrow + "px " + mono;
ctx.fillText(b.item.type.toUpperCase(), b.x + 16, b.y + 8 + eyebrow);
ctx.fillStyle = P.ink; ctx.font = "700 " + name + "px " + sans;
var title = clip(ctx, b.item.name + (b.item.target && b.item.target !== b.item.name ? " · " + b.item.target : ""), b.width - 32 - (k > 0.3 ? 90 : 0), "700 " + name + "px " + sans);
ctx.fillText(title, b.x + 16, b.y + 12 + eyebrow + name);
if (k > 0.3) {
ctx.fillStyle = P.muted; ctx.font = "11px " + sans;
var total = b.item.total || b.item.nodes.length;
var meta = (total > b.item.nodes.length ? fmt(b.item.nodes.length) + " of " : "") + fmt(total) + (total === 1 ? " object" : " objects");
ctx.fillText(meta, b.x + b.width - 16 - ctx.measureText(meta).width, b.y + 8 + eyebrow);
}
});
var shown = win ? win.shown : null;
ctx.lineWidth = 1 / Math.max(k, 0.5);
if (!win) {
ctx.strokeStyle = P["line-strong"]; ctx.globalAlpha = k < 0.3 ? 0.35 : 0.6; ctx.beginPath();
m.nodes.forEach(function (n) {
var b = lay.pos.get(n.key);
n.vup.forEach(function (u) {
var a = lay.pos.get(u);
if (a && (inView(a.x, a.y) || inView(b.x, b.y))) curve(ctx, a, b);
});
});
ctx.stroke(); ctx.globalAlpha = 1;
} else {
var hl = this.hover && shown.has(this.hover) ? this.hover : null;
[null, "up", "down"].forEach(function (side) {
ctx.beginPath();
var heads = [];
win.edges.forEach(function (e) {
if (e.side !== side) return;
var a = lay.pos.get(e.u), b = lay.pos.get(e.d);
curve(ctx, a, b); heads.push(b);
});
if (side === null) { ctx.strokeStyle = P["line-strong"]; ctx.lineWidth = 1 / Math.max(k, 0.6); ctx.globalAlpha = 0.75; }
else { ctx.strokeStyle = side === "up" ? P.up : P.down; ctx.lineWidth = 1.8 / Math.max(k, 0.7); ctx.globalAlpha = 1; }
ctx.stroke();
if (side !== null && k > 0.4) { ctx.beginPath(); heads.forEach(function (b) { arrow(ctx, b); }); ctx.fillStyle = ctx.strokeStyle; ctx.fill(); }
ctx.globalAlpha = 1;
});
if (hl) {
ctx.beginPath();
win.edges.forEach(function (e) { if (e.u === hl || e.d === hl) curve(ctx, lay.pos.get(e.u), lay.pos.get(e.d)); });
ctx.strokeStyle = P.ink; ctx.lineWidth = 1.6 / Math.max(k, 0.7); ctx.stroke();
}
}
var font = "11px " + sans, fontStrong = "600 11px " + sans;
this.labels = new Map();
m.nodes.forEach(function (n) {
var p = lay.pos.get(n.key);
if (!p || !inView(p.x, p.y)) return;
var colour = self.nodeColour(n, P);
if (win && win.seeds.has(n.key)) {
ctx.beginPath(); ctx.arc(p.x, p.y, 10, 0, 7); ctx.fillStyle = P["blue-soft"]; ctx.fill();
ctx.lineWidth = 2 / Math.max(k, 0.8); ctx.strokeStyle = P.ink; ctx.stroke();
}
glyph(ctx, n.kind, p.x, p.y, colour, P);
self.marks(ctx, n, p, P);
if (labels || (win && k > 0.3)) {
var seed = win && win.seeds.has(n.key);
var text = clip(ctx, n.label, lay.geometry.LABEL, seed ? fontStrong : font);
ctx.font = seed ? fontStrong : font;
var half = ctx.measureText(text).width / 2;
ctx.lineJoin = "round"; ctx.lineWidth = 3; ctx.strokeStyle = P.band; ctx.strokeText(text, p.x - half, p.y + LABEL_DROP);
ctx.fillStyle = P.ink;
ctx.fillText(text, p.x - half, p.y + LABEL_DROP);
self.labels.set(n.key, { x0: p.x - half, x1: p.x + half });
}
});
this.markers = [];
if (win) {
ctx.font = "600 9.5px " + mono;
win.more.forEach(function (more, key) {
var p = lay.pos.get(key);
if (!inView(p.x, p.y)) return;
var label = self.labels.get(key) || { x0: p.x - 8, x1: p.x + 8 }, y = p.y + LABEL_DROP - 4;
if (more.up.length) self.marker(ctx, P, key, "up", more.up, label.x0 - 6, y);
if (more.down.length) self.marker(ctx, P, key, "down", more.down, label.x1 + 6, y);
});
}
};
GraphView.prototype.nodeColour = function (n, P) {
if (this.o.mode !== "load") return kindColour(n.kind, P);
var s = isValidation(n) ? n.test : effectiveLoad(n);
if (n.isMirrored) return P.faint;
return s ? toneColour(tone(s.result), P) : participates(n) ? P.faint : kindColour(n.kind, P);
};
/* Small status marks: a dot for a load or test that needs attention, and on
the Load page a ring for derived readiness. */
GraphView.prototype.marks = function (ctx, n, p, P) {
if (this.o.mode === "load") {
var ready = readiness(this.m, n);
if (ready.state === READINESS.READY || ready.state === READINESS.WAITING) {
ctx.beginPath(); ctx.arc(p.x, p.y, 8.5, 0, 7); ctx.lineWidth = 1.5;
ctx.setLineDash(ready.state === READINESS.WAITING ? [2, 2] : []);
ctx.strokeStyle = ready.state === READINESS.READY ? P.blue : P.amber; ctx.stroke(); ctx.setLineDash([]);
}
return;
}
var s = isValidation(n) ? n.test : effectiveLoad(n), t = s ? tone(s.result) : null;
if (t === "bad" || t === "warn" || t === "wait") {
ctx.beginPath(); ctx.arc(p.x + 6, p.y - 6, 2.8, 0, 7); ctx.fillStyle = toneColour(t, P); ctx.fill();
ctx.lineWidth = 1; ctx.strokeStyle = P.surface; ctx.stroke();
}
};
/* An expansion marker: ‹‹ N for upstream neighbours left out, ending at x, or
N ›› downstream, starting at x. */
GraphView.prototype.marker = function (ctx, P, key, side, keys, x, y) {
var text = side === "up" ? "‹‹ " + keys.length : keys.length + " ››", w = ctx.measureText(text).width + 12, left = side === "up" ? x - w : x;
ctx.beginPath(); roundRect(ctx, left, y - 7.5, w, 15, 7.5);
ctx.lineWidth = 1;
ctx.fillStyle = P["paper-deep"]; ctx.fill(); ctx.strokeStyle = P["line-strong"]; ctx.stroke();
ctx.fillStyle = P.muted; ctx.fillText(text, left + 6, y + 3.4);
this.markers.push({ key: key, side: side, keys: keys, x: left, y: y - 7.5, w: w, h: 15 });
};
function roundRect(ctx, x, y, w, h, radius) {
var rr = Math.min(radius, w / 2, h / 2);
ctx.moveTo(x + rr, y); ctx.arcTo(x + w, y, x + w, y + h, rr); ctx.arcTo(x + w, y + h, x, y + h, rr);
ctx.arcTo(x, y + h, x, y, rr); ctx.arcTo(x, y, x + w, y, rr); ctx.closePath();
}
function clip(ctx, text, width, font) {
ctx.font = font;
if (ctx.measureText(text).width <= width) return text;
var lo = 0, hi = text.length;
while (lo < hi) { var mid = (lo + hi + 1) >> 1; if (ctx.measureText(text.slice(0, mid) + "…").width <= width) lo = mid; else hi = mid - 1; }
return text.slice(0, lo) + "…";
}
/* ---- view changes --------------------------------------------------------- */
GraphView.prototype.fitRect = function (rect, maxK, animate) {
var k = Math.min(maxK || 1.2, Math.max(0.05, Math.min(this.width / (rect.w + 160), this.height / (rect.h + 120))));
var target = { k: k, x: this.width / 2 - (rect.x + rect.w / 2) * k, y: this.height / 2 - (rect.y + rect.h / 2) * k };
this.go(target, animate);
};
GraphView.prototype.fitAll = function (animate) {
this.fitRect({ x: 0, y: 0, w: this.lay.width, h: this.lay.height }, 1.1, animate);
};
/* Zoom to what is shown: the window's own layout, or the estate. */
GraphView.prototype.fitWindow = function (animate) {
if (!this.win) return this.fitAll(animate);
this.fitKeys(Array.from(this.win.shown), animate);
};
/* Keep a node where it is on screen across a change of layout. */
GraphView.prototype.pin = function (key, screen) {
var p = this.lay.pos.get(key), v = this.s.view;
if (!p || !screen) return;
this.s.view = { k: v.k, x: screen.x - p.x * v.k, y: screen.y - p.y * v.k };
this.draw();
};
GraphView.prototype.screenOf = function (key) {
var p = this.lay.pos.get(key), v = this.s.view;
return p ? { x: p.x * v.k + v.x, y: p.y * v.k + v.y } : null;
};
GraphView.prototype.fitKeys = function (keys, animate) {
var x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity, lay = this.lay;
keys.forEach(function (key) {
var p = lay.pos.get(key);
x0 = Math.min(x0, p.x - lay.geometry.LABEL / 2 - 50); y0 = Math.min(y0, p.y - 20); x1 = Math.max(x1, p.x + lay.geometry.LABEL / 2 + 50); y1 = Math.max(y1, p.y + LABEL_DROP + 12);
});
var rect = { x: x0, y: y0, w: x1 - x0, h: y1 - y0 }, k = Math.min(1.15, Math.min(this.width / (rect.w + 160), this.height / (rect.h + 120)));
if (k < 0.2 && this.win && this.win.focus) {
var p = lay.pos.get(this.win.focus);
return this.go({ k: 0.75, x: this.width / 2 - (p.x + 60) * 0.75, y: this.height / 2 - p.y * 0.75 }, animate);
}
this.fitRect(rect, 1.15, animate);
};
GraphView.prototype.go = function (target, animate) {
var self = this, from = this.s.view, run = this.run = (this.run || 0) + 1;
if (!animate || !from || !root.requestAnimationFrame) { this.s.view = target; this.draw(); return; }
var start = null;
function frame(now) {
if (run !== self.run) return;
if (start === null) start = now;
var t = Math.min(1, (now - start) / 380), e = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
self.s.view = { k: from.k + (target.k - from.k) * e, x: from.x + (target.x - from.x) * e, y: from.y + (target.y - from.y) * e };
self.paint();
if (t < 1) root.requestAnimationFrame(frame);
}
root.requestAnimationFrame(frame);
};
GraphView.prototype.zoomAt = function (factor, px, py) {
this.run = (this.run || 0) + 1;
var v = this.s.view, k = Math.min(3, Math.max(0.04, v.k * factor)), f = k / v.k;
this.s.view = { k: k, x: px - (px - v.x) * f, y: py - (py - v.y) * f };
this.draw();
};
GraphView.prototype.panBy = function (dx, dy) {
this.run = (this.run || 0) + 1;
var v = this.s.view;
this.s.view = { k: v.k, x: v.x + dx, y: v.y + dy };
this.draw();
};
/* ---- hit testing and input ------------------------------------------------ */
GraphView.prototype.world = function (cx, cy) {
var box = this.canvas.getBoundingClientRect(), v = this.s.view;
return { x: (cx - box.left - v.x) / v.k, y: (cy - box.top - v.y) / v.k, sx: cx - box.left, sy: cy - box.top };
};
GraphView.prototype.hit = function (cx, cy) {
var w = this.world(cx, cy), self = this, best = null, bestD = Infinity, slop = 6 / this.s.view.k;
for (var i = this.markers.length - 1; i >= 0; i--) {
var mk = this.markers[i];
if (w.x >= mk.x - slop && w.x <= mk.x + mk.w + slop && w.y >= mk.y - slop && w.y <= mk.y + mk.h + slop) return { marker: mk };
}
var gx = Math.floor(w.x / CELL), gy = Math.floor(w.y / CELL);
for (var dx = -3; dx <= 3; dx++) for (var dy = -1; dy <= 1; dy++) {
(self.grid.get((gx + dx) + "|" + (gy + dy)) || []).forEach(function (key) {
var p = self.lay.pos.get(key), label = self.labels && self.labels.get(key);
var near = Math.hypot(w.x - p.x, w.y - p.y);
var onLabel = label && w.x >= label.x0 && w.x <= label.x1 && w.y >= p.y + 8 && w.y <= p.y + LABEL_DROP + 5;
var d = onLabel ? 0.5 : near;
if ((near <= 9 + slop || onLabel) && d < bestD) { best = key; bestD = d; }
});
}
return best ? { node: best } : null;
};
GraphView.prototype.bind = function () {
var self = this, c = this.canvas, pointers = new Map(), drag = null, pinch = null;
c.addEventListener("pointerdown", function (e) {
pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
if (e.pointerType === "mouse") c.setPointerCapture(e.pointerId);
if (pointers.size === 1) {
var h = e.pointerType !== "touch" ? self.hit(e.clientX, e.clientY) : null, p = h && h.node ? self.lay.pos.get(h.node) : null;
drag = { x: e.clientX, y: e.clientY, view: self.s.view, moved: false, touch: e.pointerType === "touch",
node: p ? h.node : null, from: p ? { x: p.x, y: p.y } : null };
}
else if (pointers.size === 2) {
var pts = Array.from(pointers.values());
pinch = { d: Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y), cx: (pts[0].x + pts[1].x) / 2, cy: (pts[0].y + pts[1].y) / 2, view: self.s.view };
drag = null;
}
});
c.addEventListener("pointermove", function (e) {
if (pointers.has(e.pointerId)) pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
if (pinch && pointers.size === 2) {
var pts = Array.from(pointers.values()), box = c.getBoundingClientRect();
var d = Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y), cx = (pts[0].x + pts[1].x) / 2, cy = (pts[0].y + pts[1].y) / 2;
var k = Math.min(3, Math.max(0.04, pinch.view.k * d / Math.max(1, pinch.d))), f = k / pinch.view.k;
var px = pinch.cx - box.left, py = pinch.cy - box.top;
self.s.view = { k: k, x: px - (px - pinch.view.x) * f + (cx - pinch.cx), y: py - (py - pinch.view.y) * f + (cy - pinch.cy) };
self.draw();
return;
}
if (drag) {
var dx = e.clientX - drag.x, dy = e.clientY - drag.y;
if (!drag.moved && Math.hypot(dx, dy) < 4) return;
drag.moved = true;
self.hideTip();
if (drag.node) {
var at = self.lay.pos.get(drag.node), k = self.s.view.k;
at.x = drag.from.x + dx / k; at.y = drag.from.y + dy / k;
c.classList.add("wd-dragging");
self.draw();
return;
}
self.s.view = { k: drag.view.k, x: drag.view.x + dx, y: drag.view.y + (drag.touch ? 0 : dy) };
c.classList.add("wd-dragging");
self.draw();
return;
}
if (e.pointerType === "mouse") self.hoverAt(e.clientX, e.clientY);
});
function end(e) {
var wasClick = drag && !drag.moved && pointers.size === 1;
pointers.delete(e.pointerId);
c.classList.remove("wd-dragging");
if (pointers.size < 2) pinch = null;
if (wasClick && e.type === "pointerup") self.click(e.clientX, e.clientY, e.shiftKey || e.metaKey || e.ctrlKey);
if (drag && drag.node && drag.moved) {
self.index(self.lay);
if (self.o.onMove) self.o.onMove(drag.node, self.lay.pos.get(drag.node));
}
if (!pointers.size) drag = null;
}
c.addEventListener("pointerup", end);
c.addEventListener("pointercancel", end);
c.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse") { self.hover = null; self.hideTip(); self.draw(); } });
c.addEventListener("wheel", function (e) {
var box = c.getBoundingClientRect();
if (e.ctrlKey || e.metaKey) {
e.preventDefault();
self.zoomAt(Math.exp(-e.deltaY * (e.deltaMode ? 0.05 : 0.0025)), e.clientX - box.left, e.clientY - box.top);
} else if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
e.preventDefault(); self.panBy(-e.deltaX, 0);
} else if (!pageScrolls()) {
e.preventDefault();
self.zoomAt(Math.exp(-e.deltaY * (e.deltaMode ? 0.05 : 0.0025)), e.clientX - box.left, e.clientY - box.top);
} else self.flashHint();
}, { passive: false });
c.addEventListener("keydown", function (e) {
var step = 80, handled = true;
if (e.key === "ArrowLeft") self.panBy(step, 0);
else if (e.key === "ArrowRight") self.panBy(-step, 0);
else if (e.key === "ArrowUp") self.panBy(0, step);
else if (e.key === "ArrowDown") self.panBy(0, -step);
else if (e.key === "+" || e.key === "=") self.zoomAt(1.25, self.width / 2, self.height / 2);
else if (e.key === "-") self.zoomAt(0.8, self.width / 2, self.height / 2);
else if (e.key === "0") self.fitWindow(true);
else if (e.key === "Escape" && self.o.onSelect && !self.host.closest(".wd-maximised")) self.o.onSelect(null);
else handled = false;
if (handled) e.preventDefault();
});
};
function pageScrolls() {
var s = document.scrollingElement || document.documentElement;
return s.scrollHeight > s.clientHeight + 4;
}
GraphView.prototype.flashHint = function () {
var hint = this.hint;
hint.hidden = false;
clearTimeout(this.hintTimer);
this.hintTimer = setTimeout(function () { hint.hidden = true; }, 1400);
};
GraphView.prototype.click = function (cx, cy, adding) {
var h = this.hit(cx, cy);
if (!h) return;
if (h.marker && this.o.onReveal) this.o.onReveal(h.marker);
else if (h.node && this.o.onSelect) this.o.onSelect(h.node, adding);
};
GraphView.prototype.hoverAt = function (cx, cy) {
var h = this.hit(cx, cy), key = h && h.node ? h.node : null;
this.canvas.style.cursor = h ? "pointer" : "grab";
if (h && h.marker) {
this.showTip(cx, cy, [el("b", { text: h.marker.keys.length + (h.marker.side === "up" ? " more upstream" : " more downstream") }),
el("div", { "class": "wd-muted", text: "Select to show " + (h.marker.keys.length > BUDGET.REVEAL ? "the first " + BUDGET.REVEAL : h.marker.keys.length === 1 ? "it" : "them") })]);
} else if (key) {
var n = this.m.nodes.get(key), s = isValidation(n) ? n.test : effectiveLoad(n);
this.showTip(cx, cy, [el("b", { text: n.label }), el("div", { "class": "wd-muted", text: n.kind + " · " + n.item }),
s ? el("div", {}, [chip(s.result), " " + (s.completed ? stamp(s.completed) : "")]) : null]);
} else this.hideTip();
if (key !== this.hover) { this.hover = key; this.draw(); }
};
GraphView.prototype.showTip = function (cx, cy, children) {
var box = this.host.getBoundingClientRect(), tip = this.tip;
tip.textContent = "";
children.forEach(function (c) { if (c) tip.appendChild(c); });
tip.hidden = false;
tip.style.left = Math.min(box.width - 250, cx - box.left + 14) + "px";
tip.style.top = Math.min(box.height - 70, cy - box.top + 14) + "px";
};
GraphView.prototype.hideTip = function () { this.tip.hidden = true; };
function el(tag, attrs, children) {
var e = document.createElement(tag);
setAttrs(e, attrs);
(children || []).forEach(function (c) { if (c !== null && c !== undefined && c !== false) e.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
return e;
}
function setAttrs(e, attrs) {
Object.keys(attrs || {}).forEach(function (k) {
var v = attrs[k];
if (v === null || v === undefined || v === false) return;
if (k.slice(0, 2) === "on") e.addEventListener(k.slice(2), v);
else if (k === "text") e.textContent = v;
else e.setAttribute(k, v);
});
}
function fmt(n) { return n === null || n === undefined ? "—" : Number(n).toLocaleString("en-AU"); }
function duration(ms) {
if (ms === null || ms === undefined) return "—";
var s = ms / 1000;
if (s < 60) return (s < 10 ? s.toFixed(1) : Math.round(s)) + " s";
var mins = Math.floor(s / 60);
if (mins < 60) return mins + " min " + Math.round(s % 60) + " s";
var h = Math.floor(mins / 60);
return h < 48 ? h + " h " + (mins % 60) + " min" : Math.floor(h / 24) + " d " + (h % 24) + " h";
}
function stamp(t) {
if (t === null || t === undefined) return "—";
return new Date(t).toISOString().replace("T", " ").slice(0, 19) + " UTC";
}
function ago(t, now) {
if (t === null || t === undefined) return "never";
var s = Math.max(0, (now - t) / 1000);
if (s < 90) return Math.round(s) + " s ago";
if (s < 5400) return Math.round(s / 60) + " min ago";
if (s < 172800) return Math.round(s / 3600) + " h ago";
return Math.round(s / 86400) + " days ago";
}
function chip(result, label) {
return el("span", { "class": "wd-chip wd-" + tone(result) }, [label || result || "No status"]);
}
function severityChip(severity, unobserved) {
if (unobserved) return el("span", { "class": "wd-chip wd-none", text: "Unobserved" });
return el("span", { "class": "wd-chip wd-" + ({ red: "bad", amber: "warn", green: "ok" }[severity]), text: { red: "Red", amber: "Amber", green: "Green" }[severity] });
}
function kindMark(kind) { return el("i", { "class": "wd-kind wd-kind-" + String(kind).toLowerCase().replace(/\s+/g, "-"), title: String(kind), "aria-hidden": "true" }); }
function state() {
root.__WD_STATE = root.__WD_STATE || {};
return root.__WD_STATE;
}
function pageState(name) { var s = state(); s[name] = s[name] || {}; return s[name]; }
function weaveMark() { return el("span", { "class": "wd-mark", "aria-hidden": "true" }, [el("i"), el("i"), el("i"), el("i")]); }
var PAGE_TITLES = {
overview: "Overview", health: "Health", orchestration: "Load orchestration", gantt: "Gantt",
performance: "Performance", entities: "Entity dictionary", semantic: "Semantic model"
};
/* The header every page shares: the catalogue's own name, where it lives, and
the two times a reader needs apart, when this was queried and when work
last processed. */
function shell(mount, m) {
var s = state();
var title = m.catalogue.name || "Weaver catalogue";
var context = [m.catalogue.workspace ? "Workspace " + m.catalogue.workspace : null,
m.catalogue.version ? "Weaver " + m.catalogue.version : null].filter(Boolean).join(" · ");
var processed = latestProcessed(m);
var head = el("header", { "class": "wd-top" }, [
el("div", { "class": "wd-brand" }, [weaveMark(), el("div", {}, [
el("div", { "class": "wd-eyebrow", text: "Catalogue · " + (PAGE_TITLES[m.page] || m.page) }),
el("h1", { text: title }),
context ? el("div", { "class": "wd-context", text: context }) : null
])]),
el("span", { "class": "wd-grow" }),
el("dl", { "class": "wd-times" }, [
el("dt", { text: "Queried" }), el("dd", { text: stamp(m.at) }),
processed === undefined ? null : el("dt", { text: "Last processed" }),
processed === undefined ? null : el("dd", { text: processed ? stamp(processed) + " · " + ago(processed, m.at) : "nothing has been processed" })
])
]);
mount.appendChild(head);
if (m.problems.length) {
mount.appendChild(el("div", { "class": "wd-banner wd-banner-bad" }, [
el("b", { text: "Some catalogue data could not be read. " }),
m.problems.slice(0, 3).join(" ") + (m.problems.length > 3 ? " (" + (m.problems.length - 3) + " more)" : "")
]));
}
if (m.graphGaps && m.graphGaps.size) {
var gaps = Array.from(m.graphGaps.keys()).sort(compare);
mount.appendChild(el("div", { "class": "wd-banner wd-banner-warn wd-banner-top" }, [
el("b", { text: "Lineage may be out of date. " }),
fmt(Array.from(m.graphGaps.values()).reduce(function (a, b) { return a + b; }, 0)) + " certified objects in " + gaps.join(", ") +
" have no recorded lineage. Build " + (gaps.length === 1 ? "that item" : "those items") + " again to record it."
]));
}
var body = el("main", { "class": "wd-body" });
mount.appendChild(body);
return body;
}
/* The latest processed load, test or workflow, or undefined when the page
carries none of them. */
function latestProcessed(m) {
if (!m.tables.loads && !m.tables.tests && !m.tables.workflows) return undefined;
var latest = null;
m.nodes.forEach(function (n) {
[n.load, n.test].forEach(function (s) { if (s && s.result !== "Pending" && s.completed !== null) latest = later(latest, s.completed); });
});
(m.workflows || []).forEach(function (w) { latest = later(latest, w.completed); });
return latest;
}
/* The box that clips a node as the reader scrolls: the nearest scrolling
ancestor, or the viewport. Power BI's HTML Content scrolls an element, not
the window, and an element's scroll event does not reach the window. */
function scrollBox(node) {
for (var n = node.parentElement; n && n !== document.body && n !== document.documentElement; n = n.parentElement) {
var o = root.getComputedStyle(n).overflowY;
if ((o === "auto" || o === "scroll") && n.scrollHeight > n.clientHeight) return n;
}
return null;
}
/* The part of the page a node can be seen in: inside its scrolling box and
below the sticky page header. */
function clipRect(node) {
var box = scrollBox(node), height = root.innerHeight || 800, head = document.querySelector(".wd-top");
var top = 0, bottom = height;
if (box) { var r = box.getBoundingClientRect(); top = Math.max(0, r.top); bottom = Math.min(height, r.bottom); }
if (head) top = Math.max(top, head.getBoundingClientRect().bottom);
return { top: top, bottom: bottom };
}
/* Calls f on any scroll, in the window or an element, until node leaves the page. */
function onAnyScroll(node, f) {
function listener() { if (!node.isConnected) document.removeEventListener("scroll", listener, true); else f(); }
document.addEventListener("scroll", listener, { capture: true, passive: true });
}
/* Canvas pixels per CSS pixel. The Power BI Service fits a page to its window
by scaling the visual's frame, which enlarges a canvas drawn at the device
ratio alone. The frame scales up to the screen's size at most, and the
screen stays the same through full screen, so the canvas draws that many
times over, within a pixel budget. An expanded visual is not scaled and its
layout width is the screen's, so it draws near the device ratio. */
function canvasRatio(width, height) {
var device = root.devicePixelRatio || 1, scr = root.screen || {};
var frame = Math.max(1, Math.min((scr.availWidth || 0) / Math.max(1, root.innerWidth || 0) || 1,
(scr.availHeight || 0) / Math.max(1, root.innerHeight || 0) || 1));
var wanted = Math.min(6, Math.max(2, device * 1.5, device * frame));
return Math.max(device, Math.min(wanted, Math.sqrt(20e6 / Math.max(1, width * height))));
}
function redraw() { if (root.__WD_REDRAW) root.__WD_REDRAW(); }
function section(title, children, attrs) {
return el("section", Object.assign({ "class": "wd-section" }, attrs || {}), [title ? el("h2", { "class": "wd-h", text: title }) : null].concat(children || []));
}
function empty(text) { return el("div", { "class": "wd-empty", text: text }); }
/* ---- search ----------------------------------------------------------------- */
/* A term holding * matches a whole name, each * standing for any run of
characters: dim* starts with dim, *fact* contains fact. Null without one. */
function wildcard(term) {
if (term.indexOf("*") < 0) return null;
return new RegExp("^" + term.split("*").map(function (part) { return part.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }).join(".*") + "$");
}
function searchNodes(m, query, limit) {
var terms = String(query || "").toLowerCase().split(/\s+/).filter(Boolean);
if (!terms.length) return [];
var found = [];
m.nodes.forEach(function (n) {
var label = n.label.toLowerCase(), item = n.item.toLowerCase(), desc = n.desc.toLowerCase(),
full = (n.schema + "." + n.object).toLowerCase(), score = 0;
for (var i = 0; i < terms.length; i++) {
var t = terms[i], s = 0, w = wildcard(t);
if (w) s = w.test(label) || w.test((n.object || "").toLowerCase()) || w.test(full) ? 70 : 0;
else if (label === t || n.object && n.object.toLowerCase() === t) s = 100;
else if (label.indexOf(t) === 0 || (n.object || "").toLowerCase().indexOf(t) === 0) s = 80;
else if ((" " + label.replace(/[._/\-]/g, " ")).indexOf(" " + t) >= 0) s = 60;
else if (label.indexOf(t) >= 0 || full.indexOf(t) >= 0) s = 40;
else if (item.indexOf(t) >= 0) s = 25;
else if (n.kind.toLowerCase() === t) s = 20;
else if (desc.indexOf(t) >= 0) s = 10;
if (!s) return;
score += s;
}
found.push({ node: n, score: score });
});
found.sort(function (a, b) {
return b.score - a.score || a.node.label.length - b.node.label.length || compare(a.node.label, b.node.label) || compare(a.node.key, b.node.key);
});
return found.slice(0, limit || 12).map(function (f) { return f.node; });
}
function searchBox(options) {
var input = el("input", { "class": "wd-search", type: "search", placeholder: options.placeholder || "Search", "aria-label": options.placeholder || "Search", autocomplete: "off", spellcheck: "false" });
var list = el("ul", { "class": "wd-results", role: "listbox", hidden: "hidden" }), results = [], active = 0;
function render() {
list.textContent = "";
list.hidden = !results.length;
results.forEach(function (r, i) {
list.appendChild(el("li", { role: "option", "aria-selected": String(i === active), "class": "wd-result",
onmousedown: function (e) { e.preventDefault(); choose(r, e.shiftKey || e.metaKey || e.ctrlKey); } },
[el("span", { "class": "wd-result-label" }, [r.kind ? kindMark(r.kind) : null, r.label]),
el("span", { "class": "wd-result-meta", text: r.meta }),
r.desc ? el("span", { "class": "wd-result-desc", text: r.desc }) : null]));
});
}
function choose(r, adding) {
input.value = ""; results = []; render(); input.blur();
if (r.pattern) options.onPattern(r.pattern); else options.onPick(r, adding);
}
input.addEventListener("input", function () {
var q = input.value.trim();
results = options.find(input.value);
if (options.onPattern && q.indexOf("*") >= 0) results = [{ pattern: q, label: "Select every match for " + q, meta: "Adds them to the selection" }].concat(results);
active = 0; render();
});
input.addEventListener("keydown", function (e) {
if (e.key === "ArrowDown") { active = Math.min(results.length - 1, active + 1); render(); e.preventDefault(); }
else if (e.key === "ArrowUp") { active = Math.max(0, active - 1); render(); e.preventDefault(); }
else if (e.key === "Enter" && results[active]) choose(results[active], e.shiftKey || e.metaKey || e.ctrlKey);
else if (e.key === "Escape") { input.value = ""; results = []; render(); }
});
input.addEventListener("blur", function () { setTimeout(function () { list.hidden = true; }, 150); });
input.addEventListener("focus", function () { if (results.length) list.hidden = false; });
return el("div", { "class": "wd-searchbox" }, [input, list]);
}
/* Every object a search matches, for a wildcard term in the selection. */
function nodeMatches(m, query) { return searchNodes(m, query, Infinity).map(function (n) { return n.key; }); }
function nodeSearch(m, onPick, onPattern) {
return searchBox({
placeholder: "Search " + fmt(m.nodes.size) + " objects · * matches any text · Shift adds",
find: function (q) {
return searchNodes(m, q, 12).map(function (n) { return { key: n.key, kind: n.kind, label: n.label, meta: n.kind + " · " + n.item, desc: n.desc }; });
},
onPick: function (r, adding) { onPick(r.key, adding); },
onPattern: onPattern
});
}
function segmented(label, values, value, onChange, display) {
var group = el("div", { "class": "wd-seg", role: "radiogroup", "aria-label": label }, [el("span", { "class": "wd-seg-label", text: label })]);
values.forEach(function (v) {
group.appendChild(el("button", { "class": "wd-seg-btn", type: "button", role: "radio", "aria-checked": String(v === value),
onclick: function () {
Array.prototype.forEach.call(group.querySelectorAll("button"), function (b) { b.setAttribute("aria-checked", "false"); });
this.setAttribute("aria-checked", "true");
onChange(v);
} }, [display ? display(v) : String(v)]));
});
return group;
}
function depthLabel(d) { return d < 0 ? "Max" : String(d); }
/* ---- object details ----------------------------------------------------------- */
function nodeLink(m, key, onOpen) {
var n = m.nodes.get(key);
return el("button", { "class": "wd-link", type: "button", title: n.item + " · " + qualified(n), onclick: function () { onOpen(key); } },
[kindMark(n.kind), n.label, el("span", { "class": "wd-link-meta", text: itemName(n.item) })]);
}
function details(panel, m, key, options) {
options = options || {};
panel.textContent = "";
var n = m.nodes.get(key);
if (!n) { panel.appendChild(empty(options.emptyText || "Select an object to see its details.")); return; }
var open = options.onOpen || function () {};
panel.appendChild(el("div", { "class": "wd-eyebrow" }, [kindMark(n.kind), " " + n.kind]));
panel.appendChild(el("h2", { "class": "wd-detail-title", text: n.label }));
panel.appendChild(el("div", { "class": "wd-mono wd-muted", text: n.item + " · " + qualified(n) }));
panel.appendChild(el("p", { "class": n.desc ? "wd-desc" : "wd-desc wd-muted", text: n.desc || "No description is declared." }));
var s = isValidation(n) ? n.test : effectiveLoad(n), carries = !!m.tables.loads;
var facts = el("dl", { "class": "wd-facts" });
function fact(label, value) { facts.appendChild(el("dt", { text: label })); facts.appendChild(el("dd", {}, [value])); }
if (carries && n.isMirrored) fact("Load", el("span", { "class": "wd-muted", text: "Recorded in the catalogue this one mirrors" }));
else if (carries && s) {
fact(isValidation(n) ? "Last run" : "Last load", el("span", {}, [chip(s.result), " " + stamp(s.completed)]));
if (s.duration !== null && s.duration !== undefined) fact("Duration", duration(s.duration));
if (isValidation(n) && s.failures) fact("Failing rows", fmt(s.failures));
if (s.workflow) fact("Workflow", el("span", { "class": "wd-mono", text: s.workflow }));
} else if (carries && (participates(n) || isValidation(n))) fact(isValidation(n) ? "Last run" : "Last load", el("span", { "class": "wd-muted", text: "Nothing has been processed since it was built" }));
if (carries && isLoadSubject(n)) {
var ready = readiness(m, n);
fact("Readiness", el("span", {}, [el("span", { "class": "wd-chip wd-" + readinessTone(ready.state), text: ready.state }),
ready.waitingOn.length ? " waiting on " + ready.waitingOn.slice(0, 3).map(function (w) { return w.label; }).join(", ") + (ready.waitingOn.length > 3 ? " and " + (ready.waitingOn.length - 3) + " more" : "") : ""]));
}
if (n.built) fact("Built", stamp(n.built));
if (n.isStatic) fact("Static", "Loaded once");
panel.appendChild(facts);
if (options.health) {
var mine = options.health.all.filter(function (f) { return f.node === n; });
if (mine.length) {
panel.appendChild(el("h3", { "class": "wd-h3", text: "Health" }));
panel.appendChild(el("ul", { "class": "wd-findings" }, mine.map(function (f) {
return el("li", {}, [severityChip(f.severity, f.unobserved), " " + f.message]);
})));
}
}
var validations = n.vdown.filter(function (d) { return isValidation(m.nodes.get(d)); });
if (validations.length) {
panel.appendChild(el("h3", { "class": "wd-h3", text: "Tests and Assumptions" }));
panel.appendChild(el("ul", { "class": "wd-list" }, validations.map(function (d) {
var t = m.nodes.get(d);
return el("li", {}, [nodeLink(m, d, open), el("span", { "class": "wd-grow" }), carries ? chip(t.test ? t.test.result : null, t.test ? null : "Not run") : null]);
})));
}
[["Reads", n.vup.filter(function (u) { return !isValidation(m.nodes.get(u)); })],
["Read by", n.vdown.filter(function (d) { return !isValidation(m.nodes.get(d)); })]].forEach(function (pair) {
if (!pair[1].length) return;
var sorted = pair[1].slice().sort(function (a, b) { return compare(m.nodes.get(a).label, m.nodes.get(b).label); });
panel.appendChild(el("h3", { "class": "wd-h3", text: pair[0] + " · " + pair[1].length }));
panel.appendChild(el("ul", { "class": "wd-list" }, sorted.slice(0, 40).map(function (k) { return el("li", {}, [nodeLink(m, k, open)]); })
.concat(sorted.length > 40 ? [el("li", { "class": "wd-muted", text: (sorted.length - 40) + " more" })] : [])));
});
if (n.missing.length) {
panel.appendChild(el("h3", { "class": "wd-h3", text: "Reads objects not in lineage · " + n.missing.length }));
panel.appendChild(el("p", { "class": "wd-muted", text: "Not installed, or in an item no Build has recorded lineage for since." }));
panel.appendChild(el("ul", { "class": "wd-list wd-mono" }, n.missing.map(function (id) { return el("li", { text: id }); })));
}
if (n.stubs.length) {
panel.appendChild(el("h3", { "class": "wd-h3", text: "Reads outside Weaver · " + n.stubs.length }));
panel.appendChild(el("ul", { "class": "wd-list wd-mono" }, n.stubs.map(function (ref) { return el("li", { text: ref }); })));
}
if (options.columns) {
var cols = options.columns.get(n.id) || [];
if (cols.length) {
panel.appendChild(el("h3", { "class": "wd-h3", text: "Described columns · " + cols.length }));
panel.appendChild(el("dl", { "class": "wd-columns" }, cols.reduce(function (all, c) {
return all.concat([el("dt", { text: c.column }), el("dd", { text: c.description || "" })]);
}, [])));
}
}
}
function readinessTone(state) {
return { Current: "ok", Ready: "next", Waiting: "wait", "Loaded elsewhere": "none", "Not loaded here": "none" }[state] || "none";
}
/* A table for a list of records, with optional sorting and a row limit. */
function dataTable(columns, rows, options) {
options = options || {};
var limit = options.limit || 200, sortBy = options.sort || null, desc = options.desc !== false;
var wrap = el("div", { "class": "wd-table-wrap" });
function render() {
wrap.textContent = "";
var sorted = rows.slice();
if (sortBy) {
var col = columns.filter(function (c) { return c.key === sortBy; })[0];
sorted.sort(function (a, b) {
var x = col.sort ? col.sort(a) : col.value(a), y = col.sort ? col.sort(b) : col.value(b);
var r = typeof x === "number" || typeof y === "number" ? (x === null ? -Infinity : x) - (y === null ? -Infinity : y) : compare(x, y);
return desc ? -r : r;
});
}
var table = el("table", { "class": "wd-table" }, [
el("thead", {}, [el("tr", {}, columns.map(function (c) {
return el("th", { "class": c.numeric ? "wd-num" : null, scope: "col", "aria-sort": c.key === sortBy ? (desc ? "descending" : "ascending") : null },
[c.sortable === false ? c.title : el("button", { type: "button", "class": "wd-sort", onclick: function () {
if (sortBy === c.key) desc = !desc; else { sortBy = c.key; desc = !!c.numeric; }
render();
} }, [c.title])]);
}))]),
el("tbody", {}, sorted.slice(0, limit).map(function (row) {
return el("tr", { "class": options.onRow ? "wd-clickable" : null, onclick: options.onRow ? function () { options.onRow(row); } : null },
columns.map(function (c) {
var v = c.render ? c.render(row) : c.value(row);
return el("td", { "class": c.numeric ? "wd-num" : c.mono ? "wd-mono" : null }, [v === null || v === undefined ? "—" : typeof v === "object" ? v : String(v)]);
}));
}))
]);
wrap.appendChild(table);
if (sorted.length > limit) wrap.appendChild(el("div", { "class": "wd-more-rows", text: "Showing " + fmt(limit) + " of " + fmt(sorted.length) + ". Search or sort to find the rest." }));
if (!sorted.length) wrap.appendChild(empty(options.emptyText || "Nothing to show."));
}
render();
return wrap;
}
var DEPTHS = [0, 1, 2, -1];
/* One graph with its toolbar, status line and details. With nothing selected it
shows the estate, or one item. A selection filters it to the selected objects
and their lineage to the chosen depths, laid out on their own; a marker on a
shown object expands the neighbours left out. Nodes can be dragged, and the
graph can fill the page. Nodes are coloured by kind, or by last outcome with
derived readiness ringed. */
function graphWorkspace(body, m, options) {
var s = pageState(options.page), estate = layoutEstate(m);
s.selection = (s.selection || (s.focus ? [s.focus] : [])).filter(function (k) { return m.nodes.has(k); });
if (!s.focus || s.selection.indexOf(s.focus) < 0) s.focus = s.selection[s.selection.length - 1] || null;
if (s.up === undefined) s.up = 1;
if (s.down === undefined) s.down = 1;
if (s.item && !m.items.has(s.item)) s.item = null;
s.expanded = (s.expanded || []).filter(function (k) { return m.nodes.has(k); });
s.moved = s.moved || {};
s.patterns = s.patterns || [];
var matched = new Map();
function matches(q) { if (!matched.has(q)) matched.set(q, nodeMatches(m, q)); return matched.get(q); }
/* The selected objects and every match of each wildcard term. */
function seeds() {
var out = s.selection.slice(), seen = new Set(out);
s.patterns.forEach(function (q) { matches(q).forEach(function (k) { if (!seen.has(k)) { seen.add(k); out.push(k); } }); });
return out;
}
var health = options.health ? assessHealth(m) : null;
s.mode = s.mode || options.mode;
var view, f = workspaceFrame(s, function () { if (view) view.resize(); });
var host = f.host, side = f.side, line = f.line, legendHost = f.legend;
function within() {
return s.item ? new Set(m.items.get(s.item).nodes.map(function (n) { return n.key; })) : null;
}
/* A plain choice replaces the selection; Shift, Ctrl or ⌘ adds or removes. */
function select(key, adding) {
if (!key) { s.selection = []; s.patterns = []; }
else if (adding) {
var at = s.selection.indexOf(key);
if (at >= 0) s.selection.splice(at, 1); else s.selection.push(key);
} else s.selection = [key];
if (key && s.item && m.nodes.get(key).item !== s.item) { s.item = null; itemPicker.value = ""; }
s.focus = key && s.selection.indexOf(key) >= 0 ? key : s.selection[s.selection.length - 1] || null;
s.expanded = []; s.moved = {};
apply(true);
}
/* A wildcard term joins the selection, whatever else is selected. */
function addPattern(q) {
if (s.patterns.indexOf(q) < 0) s.patterns.push(q);
s.expanded = []; s.moved = {};
apply(true);
}
function removePattern(q) {
s.patterns = s.patterns.filter(function (p) { return p !== q; });
s.expanded = []; s.moved = {};
apply(true);
}
/* A marker expands the neighbours it counts, leaving its object where it is. */
function expand(marker) {
var screen = view.screenOf(marker.key);
s.expanded = s.expanded.concat(revealFrom(m, marker.keys).filter(function (k) { return s.expanded.indexOf(k) < 0; }));
apply(false);
view.pin(marker.key, screen);
}
function moved(key, p) { s.moved[key] = { x: p.x, y: p.y }; saveState(); }
function apply(refit) {
var only = within();
var seed = seeds(), win = seed.length || only ? focusWindow(m, seed, s.up, s.down, s.expanded, only) : null;
var lay = win ? layoutEstate(subModel(m, win.shown), WINDOW_GEOMETRY) : layoutEstate(m);
Object.keys(s.moved).forEach(function (k) { var p = lay.pos.get(k); if (p) { p.x = s.moved[k].x; p.y = s.moved[k].y; } });
view.setWindow(win, lay);
status(win);
renderChips();
details(side, m, s.focus, { onOpen: select, health: health, emptyText: options.empty });
if (refit) { if (win) view.fitWindow(true); else view.fitAll(true); }
saveState();
}
function renderChips() {
selectionChips(f.chips, s.selection, s.focus, function (key) { var n = m.nodes.get(key); return { kind: n.kind, label: n.label, title: n.item + " · " + qualified(n) }; },
function (key) { s.focus = key; details(side, m, key, { onOpen: select, health: health }); renderChips(); view.fitKeys([key], true); }, select,
{ list: s.patterns, count: function (q) { return matches(q).length; }, remove: removePattern });
}
function status(win) {
line.textContent = "";
if (!win) {
line.appendChild(document.createTextNode(fmt(m.nodes.size) + " objects in " + fmt(estate.bands.length) + " items. Search or select an object to follow its lineage."));
return;
}
var parts = [fmt(win.shown.size) + " of " + fmt(m.nodes.size) + " objects shown" + (win.seeds.size > 1 ? " · " + win.seeds.size + " selected" : "")];
if (win.expanded.size) parts.push(fmt(win.expanded.size) + " expanded");
if (win.hidden) parts.push(fmt(win.hidden) + " more beside them; select a ‹‹ or ›› marker to expand");
if (win.truncated) parts.push(el("b", { "class": "wd-warn-text", text: "lineage cut to the " + fmt(win.lineage.size) + " nearest of " + fmt(win.reach) + "; lower a depth" }));
if (win.edgesDropped) parts.push(el("b", { "class": "wd-warn-text", text: win.edgesDropped + " edges not drawn" }));
parts.forEach(function (p, i) { if (i) line.appendChild(document.createTextNode(" · ")); line.appendChild(typeof p === "string" ? document.createTextNode(p) : p); });
}
var itemPicker = el("select", { "class": "wd-select", "aria-label": "Item", onchange: function () {
s.item = this.value || null; s.expanded = []; s.moved = {};
if (s.item) s.selection = s.selection.filter(function (k) { return m.nodes.get(k).item === s.item; });
s.focus = s.selection[s.selection.length - 1] || null;
apply(true);
} }, [el("option", { value: "", text: "Every item" })].concat(estate.bands.map(function (b) {
return el("option", { value: b.item.label, selected: b.item.label === s.item ? "selected" : null, text: b.item.label });
})));
if (options.above) body.appendChild(options.above);
f.mount(body, [
nodeSearch(m, select, addPattern),
itemPicker,
segmented("Up", DEPTHS, s.up, function (d) { s.up = d; s.expanded = []; s.moved = {}; apply(true); }, depthLabel),
segmented("Down", DEPTHS, s.down, function (d) { s.down = d; s.expanded = []; s.moved = {}; apply(true); }, depthLabel),
segmented("Colour", ["load", "kind"], s.mode, function (v) {
s.mode = v; view.o.mode = v; view.draw(); legendHost.textContent = ""; legendHost.appendChild(legend(v)); saveState();
}, function (v) { return v === "load" ? "Outcome" : "Kind"; }),
el("span", { "class": "wd-grow" }),
el("div", { "class": "wd-zoom" }, [
el("button", { "class": "wd-icon", type: "button", title: "Zoom out", "aria-label": "Zoom out", onclick: function () { view.zoomAt(0.8, view.width / 2, view.height / 2); } }, ["−"]),
el("button", { "class": "wd-icon", type: "button", title: "Zoom in", "aria-label": "Zoom in", onclick: function () { view.zoomAt(1.25, view.width / 2, view.height / 2); } }, ["+"]),
el("button", { "class": "wd-text-btn", type: "button", title: "Fit what is shown", onclick: function () { view.fitWindow(true); } }, ["Fit"]),
el("button", { "class": "wd-text-btn", type: "button", title: "Show the whole estate", onclick: function () {
s.item = null; itemPicker.value = ""; select(null);
} }, ["Estate"])
])
]);
legendHost.appendChild(legend(s.mode));
if (!m.nodes.size) { host.appendChild(empty("The catalogue records no installed objects yet. Build a project to see its graph.")); return; }
var fresh = !s.view;
view = new GraphView(host, m, estate, { state: s, mode: s.mode, onSelect: select, onReveal: expand, onMove: moved, label: options.label });
apply(false);
if (fresh || !view.showing(s.focus)) { if (s.selection.length || s.patterns.length || s.item) view.fitWindow(false); else view.fitAll(false); }
return { select: select };
}
/* The frame both graph pages share: a toolbar, the selection as chips, a status
line, and the drawing beside its details, with a control that fills the page
with the drawing alone. */
function workspaceFrame(s, onResize) {
var f = { frame: el("div", { "class": "wd-workspace" }), bar: el("div", { "class": "wd-toolbar" }),
chips: el("div", { "class": "wd-chips", "aria-label": "Selection" }), line: el("div", { "class": "wd-status-line" }),
host: el("div", { "class": "wd-graph" }), legend: el("div"), side: el("aside", { "class": "wd-side" }) };
var maximise = el("button", { "class": "wd-icon wd-maximise", type: "button" });
function set(on) {
s.maximised = on;
f.frame.classList.toggle("wd-maximised", on);
maximise.textContent = on ? "⤡" : "⤢";
maximise.title = on ? "Restore (Esc)" : "Fill the page";
maximise.setAttribute("aria-label", maximise.title);
onResize();
saveState();
}
maximise.addEventListener("click", function () { set(!s.maximised); });
document.addEventListener("keydown", function (e) { if (e.key === "Escape" && s.maximised && f.frame.isConnected) set(false); });
f.mount = function (body, tools) {
tools.forEach(function (t) { if (t) f.bar.appendChild(t); });
f.host.appendChild(maximise);
[f.bar, f.chips, f.line, el("div", { "class": "wd-split" }, [el("div", { "class": "wd-graph-col" }, [f.host, f.legend]), f.side])]
.forEach(function (c) { f.frame.appendChild(c); });
body.appendChild(f.frame);
set(!!s.maximised);
};
return f;
}
/* The selection as chips: a name focuses its object, × removes it. select is
the page's select(key, adding). Each wildcard term in patterns is a chip of
its own, counting what it matches. */
function selectionChips(chips, selection, focus, describe, onFocus, select, patterns) {
var terms = patterns ? patterns.list : [];
chips.textContent = "";
chips.hidden = !selection.length && !terms.length;
terms.forEach(function (q) {
var count = patterns.count(q);
chips.appendChild(el("span", { "class": "wd-chip-select wd-chip-pattern" }, [
el("span", { "class": "wd-chip-name", title: "Every match for " + q, text: q + " · " + fmt(count) }),
el("button", { type: "button", "class": "wd-chip-remove", "aria-label": "Remove " + q, onclick: function () { patterns.remove(q); } }, ["×"])
]));
});
selection.forEach(function (key) {
var d = describe(key);
chips.appendChild(el("span", { "class": "wd-chip-select" + (key === focus ? " wd-current" : "") }, [
el("button", { type: "button", "class": "wd-chip-name", title: d.title, onclick: function () { onFocus(key); } }, [kindMark(d.kind), d.label]),
el("button", { type: "button", "class": "wd-chip-remove", "aria-label": "Remove " + d.label, onclick: function () { select(key, true); } }, ["×"])
]));
});
if (selection.length + terms.length > 1) chips.appendChild(el("button", { type: "button", "class": "wd-text-btn wd-chip-clear", onclick: function () { select(null); } }, ["Clear"]));
}
function legend(mode) {
var entries = mode === "load" ? [
["swatch wd-ok", "Last load succeeded"], ["swatch wd-bad", "Failed, error or blocked"], ["swatch wd-warn", "Rejected rows or pending"],
["swatch wd-none", "Nothing processed, or loaded elsewhere"], ["ring wd-next", "Ready: dependencies processed"], ["ring wd-wait", "Waiting on a dependency"]
] : [
["kind wd-kind wd-kind-table", "Table"], ["kind wd-kind wd-kind-view", "View"], ["kind wd-kind wd-kind-folder", "Folder"], ["kind wd-kind wd-kind-shortcut", "Shortcut"],
["kind wd-kind wd-kind-test", "Test"], ["kind wd-kind wd-kind-assumption", "Assumption"], ["kind wd-kind wd-kind-semantic-model", "Semantic model"], ["kind wd-kind wd-kind-report", "Report"],
["line wd-up", "Upstream"], ["line wd-down", "Downstream"], ["dot wd-bad", "Needs attention"]
];
return el("div", { "class": "wd-legend" }, entries.map(function (e) {
return el("span", { "class": "wd-key" }, [el("i", { "class": "wd-key-" + e[0] }), e[1]]);
}).concat([el("span", { "class": "wd-key" }, [el("i", { "class": "wd-key-more", text: "3 ››" }), "neighbours not shown: select to expand"])]));
}
function orchestrationPage(body, m) {
var counts = {}, failed = [], ready = [], waiting = [];
m.nodes.forEach(function (n) {
if (!isLoadSubject(n)) return;
var r = readiness(m, n), s = effectiveLoad(n);
counts[r.state] = (counts[r.state] || 0) + 1;
if (s && LOAD_RED.indexOf(s.result) >= 0) failed.push(n);
if (r.state === READINESS.READY) ready.push({ n: n, r: r });
if (r.state === READINESS.WAITING) waiting.push({ n: n, r: r });
});
var latest = (m.workflows || [])[0];
var tiles = el("div", { "class": "wd-tiles" }, [
tile("Current", counts[READINESS.CURRENT] || 0, "processed after every dependency", "ok"),
tile("Ready", counts[READINESS.READY] || 0, "behind, with every dependency processed", "next"),
tile("Waiting", counts[READINESS.WAITING] || 0, "a dependency has not been processed", "wait"),
tile("Last outcome failed", failed.length, "Failed, Error or Blocked", failed.length ? "bad" : "ok"),
tile("Loaded elsewhere", counts[READINESS.ELSEWHERE] || 0, "mirrored; not read here", "none"),
latest ? tile("Latest workflow", duration((latest.completed || 0) - (latest.started || 0)), fmt(latest.records) + " processed records · " + ago(latest.completed, m.at), latest.failed ? "bad" : "none") : null
]);
var note = el("p", { "class": "wd-note", text: "Readiness is derived from the recorded state of each object's nearest loadable dependencies. It is not a queue: the catalogue records processed work only, so nothing here is shown as running." });
graphWorkspace(body, m, { page: "orchestration", mode: "load", health: true, label: "Load orchestration graph", above: el("div", { "class": "wd-summary" }, [tiles, note]),
empty: "Search for an object, or select one in the graph, to follow its lineage, last outcome and readiness." });
var lists = el("div", { "class": "wd-columns-2" }, [
section("Ready · " + ready.length, [dataTable([
{ key: "object", title: "Object", value: function (r) { return r.n.label; } },
{ key: "item", title: "Item", value: function (r) { return r.n.item; } },
{ key: "outcome", title: "Last outcome", render: function (r) { var s = effectiveLoad(r.n); return chip(s ? s.result : null, s ? null : "None"); }, value: function (r) { var s = effectiveLoad(r.n); return s ? s.result : ""; } }
], ready, { limit: 100, sort: "object", desc: false, emptyText: "Nothing is ready to load." })]),
section("Waiting · " + waiting.length, [dataTable([
{ key: "object", title: "Object", value: function (r) { return r.n.label; } },
{ key: "on", title: "Waiting on", value: function (r) { return r.r.waitingOn[0].label + (r.r.unprocessed > 1 ? " and " + (r.r.unprocessed - 1) + " more" : ""); } },
{ key: "outcome", title: "Last outcome", render: function (r) { var s = effectiveLoad(r.n); return chip(s ? s.result : null, s ? null : "None"); }, value: function (r) { var s = effectiveLoad(r.n); return s ? s.result : ""; } }
], waiting, { limit: 100, sort: "object", desc: false, emptyText: "Nothing is waiting on a dependency." })])
]);
body.appendChild(lists);
}
function tile(label, value, note, toneName) {
return el("div", { "class": "wd-tile wd-tile-" + (toneName || "none") }, [
el("div", { "class": "wd-tile-label", text: label }),
el("div", { "class": "wd-tile-value", text: typeof value === "number" ? fmt(value) : value }),
note ? el("div", { "class": "wd-tile-note", text: note }) : null
]);
}
var KIND_ORDER = [KIND.FOLDER, KIND.SHORTCUT, KIND.TABLE, KIND.VIEW, KIND.MODEL, KIND.REPORT, KIND.TEST, KIND.ASSUMPTION];
function overviewPage(body, m) {
var health = assessHealth(m), s = pageState("overview");
var side = el("aside", { "class": "wd-drawer", hidden: "hidden" });
function open(key) {
s.open = key;
side.hidden = !key;
details(side, m, key, { onOpen: open, health: health });
if (key) side.insertBefore(el("button", { "class": "wd-icon wd-close", type: "button", "aria-label": "Close", onclick: function () { open(null); } }, ["×"]), side.firstChild);
}
var loadRed = health.load.filter(function (f) { return f.severity === RED; }).length;
var loadAmber = health.load.filter(function (f) { return f.severity === AMBER && !f.unobserved; }).length;
var testRed = health.tests.filter(function (f) { return f.severity === RED; }).length;
var testAmber = health.tests.filter(function (f) { return f.severity === AMBER; }).length;
body.appendChild(el("div", { "class": "wd-tiles" }, [
tile("Items", visibleItems(m).filter(function (it) { return it.nodes.length; }).length, fmt(m.nodes.size) + " installed objects", "none"),
tile("Load", loadRed ? loadRed + " red" : loadAmber ? loadAmber + " amber" : "Green", health.counts.load.subjects + " subjects · " + loadAmber + " amber", loadRed ? "bad" : loadAmber ? "wait" : "ok"),
tile("Tests", testRed ? testRed + " red" : testAmber ? testAmber + " amber" : "Green", health.counts.tests.subjects + " Tests and Assumptions", testRed ? "bad" : testAmber ? "wait" : "ok"),
tile("Build", health.build.length ? health.build.length + " red" : "Consistent", "catalogue consistency only", health.build.length ? "bad" : "ok"),
tile("Workflows, 7 days", m.workflowCount || 0, m.workflows.length ? "latest " + ago(m.workflows[0].completed, m.at) : "none in the last 7 days", "none")
]));
var inventory = section("Installed items", [itemInventory(m, open)]);
var findings = health.all.filter(function (f) { return !f.unobserved; });
var significant = section("Significant findings", [findings.length ? el("ul", { "class": "wd-findings wd-findings-wide" }, findings.slice(0, 12).map(function (f) {
return el("li", {}, [severityChip(f.severity), f.node ? nodeLink(m, f.node.key, open) : el("span", { "class": "wd-mono", text: f.label }),
el("span", { "class": "wd-muted", text: " " + f.message })]);
}).concat(findings.length > 12 ? [el("li", { "class": "wd-muted", text: (findings.length - 12) + " more on the Health page" })] : []))
: el("div", { "class": "wd-allclear", text: "No findings. Every load and Test the catalogue records has been processed, within the last 24 hours, after its dependencies." })]);
var activity = section("Recent workflows", [workflowTable(m, 8)]);
body.appendChild(el("div", { "class": "wd-overview" }, [el("div", { "class": "wd-overview-main" }, [inventory, significant, activity]), side]));
if (s.open && m.nodes.has(s.open)) open(s.open);
}
/* Each item with its objects by kind and the state of what it loads. */
function itemInventory(m, open) {
var items = visibleItems(m).filter(function (it) { return it.nodes.length || it.target; });
items.sort(function (a, b) { return typeRank(a.type) - typeRank(b.type) || compare(a.name, b.name); });
if (!items.length) return empty("Nothing is installed yet. Build a project to fill the catalogue.");
var groups = [];
items.forEach(function (it) {
var g = groups[groups.length - 1];
if (!g || g.type !== it.type) groups.push(g = { type: it.type, items: [] });
g.items.push(it);
});
return el("div", { "class": "wd-inventory" }, groups.map(function (g) {
return el("div", { "class": "wd-inv-group" }, [
el("div", { "class": "wd-eyebrow", text: g.type + " · " + g.items.length }),
el("div", { "class": "wd-inv-items" }, g.items.map(function (it) {
var byKind = {}, tones = { ok: 0, bad: 0, warn: 0, wait: 0, none: 0 }, latest = null;
it.nodes.forEach(function (n) {
byKind[n.kind] = (byKind[n.kind] || 0) + 1;
var st = isValidation(n) ? n.test : effectiveLoad(n);
if (isLoadSubject(n) || isValidation(n)) tones[st ? tone(st.result) : "none"] += 1;
if (st && st.result !== "Pending") latest = later(latest, st.completed);
});
var total = tones.ok + tones.bad + tones.warn + tones.wait + tones.none;
var first = it.nodes[0];
return el("button", { "class": "wd-inv-item", type: "button", onclick: function () { if (first) open(first.key); } }, [
el("div", { "class": "wd-inv-head" }, [el("b", { text: it.name }), it.target && it.target !== it.name ? el("span", { "class": "wd-muted", text: " → " + it.target }) : null]),
el("div", { "class": "wd-inv-kinds" }, KIND_ORDER.filter(function (k) { return byKind[k]; }).map(function (k) {
return el("span", { "class": "wd-inv-kind" }, [kindMark(k), fmt(byKind[k]) + " " + k.toLowerCase() + (byKind[k] === 1 ? "" : "s")]);
})),
total ? el("div", { "class": "wd-bar-stack", title: tones.ok + " succeeded · " + tones.bad + " failed · " + (tones.warn + tones.wait) + " pending or rejected · " + tones.none + " not processed" },
["ok", "warn", "wait", "bad", "none"].map(function (t) { return tones[t] ? el("i", { "class": "wd-" + t, style: "flex:" + tones[t] }) : null; })) : null,
el("div", { "class": "wd-inv-meta", text: total ? "Last processed " + ago(latest, m.at) : it.nodes.length ? "Nothing to load" : "No objects" })
]);
}))
]);
}));
}
function workflowTable(m, limit) {
if (!m.workflows.length) return empty("No workflow has processed a record in the last 7 days.");
return dataTable([
{ key: "completed", title: "Processed", value: function (w) { return w.completed; }, render: function (w) { return stamp(w.completed); }, numeric: true },
{ key: "span", title: "Span", value: function (w) { return (w.completed || 0) - (w.started || 0); }, render: function (w) { return duration((w.completed || 0) - (w.started || 0)); }, numeric: true },
{ key: "tasks", title: "Work", value: function (w) { return w.tasks.join(", "); } },
{ key: "records", title: "Records", value: function (w) { return w.records; }, numeric: true },
{ key: "failed", title: "Failed", value: function (w) { return w.failed; }, render: function (w) { return w.failed ? el("span", { "class": "wd-chip wd-bad", text: fmt(w.failed) }) : "0"; }, numeric: true },
{ key: "id", title: "Workflow", value: function (w) { return w.id; }, mono: true }
], m.workflows, { limit: limit, sort: "completed" });
}
function healthPage(body, m) {
var health = assessHealth(m), s = pageState("health");
s.area = s.area || "all"; s.severity = s.severity || "all";
var side = el("aside", { "class": "wd-drawer", hidden: "hidden" });
function open(key) {
side.hidden = !key;
details(side, m, key, { onOpen: open, health: health });
if (key) side.insertBefore(el("button", { "class": "wd-icon wd-close", type: "button", "aria-label": "Close", onclick: function () { open(null); } }, ["×"]), side.firstChild);
}
function sectionTile(label, area, list, subjects) {
var red = list.filter(function (f) { return f.severity === RED; }).length, amber = list.filter(function (f) { return f.severity === AMBER && !f.unobserved; }).length;
var unobserved = list.filter(function (f) { return f.unobserved; }).length, green = health.green.filter(function (f) { return f.area === area; }).length;
var worst = red ? "bad" : amber ? "wait" : "ok";
return tile(label, red ? red + " red" : amber ? amber + " amber" : "Green",
fmt(subjects) + " subjects · " + fmt(green) + " green · " + amber + " amber" + (unobserved ? " · " + unobserved + " unobserved" : ""), worst);
}
body.appendChild(el("div", { "class": "wd-tiles" }, [
sectionTile("Load", "load", health.load, health.counts.load.subjects),
sectionTile("Tests", "tests", health.tests, health.counts.tests.subjects),
sectionTile("Build", "build", health.build, health.counts.build.subjects)
]));
body.appendChild(el("p", { "class": "wd-note" }, [
"Assessed as of " + stamp(health.asOf) + ", 24 hours before the query. Build here checks what the catalogue records about itself: certification and installed validations. ",
"Physical inventory, unresolved references and a mirrored source's loads need ", el("code", { text: "weaver health" }), "."
]));
var tableHost = el("div");
function render() {
tableHost.textContent = "";
var rows = health.all.concat(health.green).filter(function (f) {
return (s.area === "all" || f.area === s.area) && (s.severity === "all" || (s.severity === "unobserved" ? f.unobserved : f.severity === s.severity && !f.unobserved));
});
tableHost.appendChild(dataTable([
{ key: "severity", title: "Severity", value: function (f) { return SEVERITY_RANK[f.severity] * 2 + (f.unobserved ? 0 : 1); }, render: function (f) { return severityChip(f.severity, f.unobserved); }, numeric: true },
{ key: "area", title: "Area", value: function (f) { return { load: "Load", tests: "Tests", build: "Build" }[f.area]; } },
{ key: "object", title: "Object", value: function (f) { return f.node ? f.node.label : f.label; }, render: function (f) { return f.node ? nodeLink(m, f.node.key, open) : el("span", { "class": "wd-mono", text: f.label }); } },
{ key: "item", title: "Item", value: function (f) { return f.node ? f.node.item : ""; } },
{ key: "result", title: "Status", value: function (f) { return f.result || ""; }, render: function (f) { return f.result ? chip(f.result) : "—"; } },
{ key: "message", title: "Finding", value: function (f) { return f.message; } },
{ key: "completed", title: "Processed", value: function (f) { return f.completed; }, render: function (f) { return f.completed ? stamp(f.completed) : "—"; }, numeric: true }
], rows, { limit: 500, sort: "severity", emptyText: "No findings match." }));
}
body.appendChild(el("div", { "class": "wd-toolbar" }, [
segmented("Area", ["all", "load", "tests", "build"], s.area, function (v) { s.area = v; render(); saveState(); }, function (v) { return { all: "All", load: "Load", tests: "Tests", build: "Build" }[v]; }),
segmented("Severity", ["all", "red", "amber", "green", "unobserved"], s.severity, function (v) { s.severity = v; render(); saveState(); }, function (v) { return { all: "All", red: "Red", amber: "Amber", green: "Green", unobserved: "Unobserved" }[v]; })
]));
render();
body.appendChild(el("div", { "class": "wd-overview" }, [el("div", { "class": "wd-overview-main" }, [tableHost]), side]));
}
function metadata(m) {
if (m.meta) return m.meta;
var t = function (name) { return m.tables[name] || []; };
function keep(r) { return !isInternal(m, r.item, r.schema); }
var md = { tables: new Map(), folders: new Map(), schemas: [], columns: new Map(), keys: new Map(), validations: new Map(),
foreignKeys: [], references: new Map(), referencedBy: new Map(), models: new Map(), hasMetadata: !!m.tables.tables, hasSemantic: !!m.tables.models };
t("tables").filter(keep).forEach(function (r) { md.tables.set(identityKey(r.item, r.schema, r.object), r); });
t("folders").filter(keep).forEach(function (r) { md.folders.set(identityKey(r.item, r.schema, r.object), r); });
md.schemas = t("schemas").filter(keep);
t("columns").filter(keep).forEach(function (r) { addTo(md.columns, identityKey(r.item, r.schema, r.object), r); });
t("keys").filter(keep).forEach(function (r) { addTo(md.keys, identityKey(r.item, r.schema, r.object), r); });
t("validations").filter(keep).forEach(function (r) { md.validations.set(identityKey(r.item, r.schema, r.object), r); });
t("foreignkeys").filter(keep).forEach(function (r) {
var fk = { from: identityKey(r.item, r.schema, r.object), to: identityKey(r.primaryitem, r.primaryschema, r.primaryobject),
fromColumns: splitList(r.columns), toColumns: splitList(r.primarycolumns), row: r };
md.foreignKeys.push(fk);
addTo(md.references, fk.from, fk); addTo(md.referencedBy, fk.to, fk);
});
md.columns.forEach(function (list) { list.sort(function (a, b) { return compare(a.column, b.column); }); });
function model(item) {
var it = m.items.get(item);
if (it && it.internal) return null;
var mo = md.models.get(item);
if (!mo) md.models.set(item, mo = { item: item, name: itemName(item), description: null, tables: new Map(), relationships: [], node: null });
return mo;
}
function table(mo, name) {
var tb = mo.tables.get(name);
if (!tb) mo.tables.set(name, tb = { model: mo, name: name, ordinal: null, description: null, mode: null, access: null, columns: [], measures: [], sources: [] });
return tb;
}
t("models").forEach(function (r) { var mo = model(r.item); if (mo) mo.description = r.description; });
t("smtables").forEach(function (r) {
var mo = model(r.item); if (!mo) return;
var tb = table(mo, r.table);
tb.ordinal = num(r.ordinal); tb.description = r.description; tb.mode = r.mode; tb.access = r.access;
});
t("smcolumns").forEach(function (r) { var mo = model(r.item); if (mo) table(mo, r.table).columns.push(r); });
t("smmeasures").forEach(function (r) { var mo = model(r.item); if (mo) table(mo, r.table).measures.push(r); });
t("smrelationships").forEach(function (r) {
var mo = model(r.item); if (!mo) return;
mo.relationships.push({ name: r.name, from: r.fromtable, fromColumn: r.fromcolumn, to: r.totable, toColumn: r.tocolumn,
fromCardinality: (r.fromcardinality || "many").toLowerCase(), toCardinality: (r.tocardinality || "one").toLowerCase(),
crossFilter: r.crossfilter, active: r.active !== "0" });
});
t("smsources").forEach(function (r) {
var mo = model(r.item); if (!mo) return;
table(mo, r.table).sources.push({ reference: r.reference, item: r.sourceitem, schema: r.sourceschema, object: r.sourceobject,
node: r.sourceitem ? m.byIdentity.get(identityKey(r.sourceitem, r.sourceschema, r.sourceobject)) || null : null });
});
md.models.forEach(function (mo) {
mo.tables.forEach(function (tb) {
tb.columns.sort(function (a, b) { return compare(a.column, b.column); });
tb.measures.sort(function (a, b) { return compare(a.measure, b.measure); });
});
var root = null;
m.nodes.forEach(function (n) { if (n.item === mo.item && n.kind === KIND.MODEL) root = n; });
mo.node = root;
});
m.meta = md;
return md;
}
function splitList(text) { return text ? String(text).split(",").map(function (s) { return s.trim(); }).filter(Boolean) : []; }
/* Tables of a model in authored TMDL order, or alphabetically. */
function modelTables(mo, order) {
var list = Array.from(mo.tables.values());
list.sort(order === "alphabetical" || list.some(function (tb) { return tb.ordinal === null; })
? function (a, b) { return compare(a.name, b.name) || (a.name < b.name ? -1 : 1); }
: function (a, b) { return a.ordinal - b.ordinal; });
return list;
}
/* Every searchable entry: items, objects, declared columns and, for semantic
models, tables, columns and measures. */
function dictionaryEntries(m) {
if (m.entries) return m.entries;
var md = metadata(m), out = [];
visibleItems(m).forEach(function (it) {
if (!it.nodes.length && !it.target) return;
out.push({ kind: "Item", label: it.name, meta: it.type + (it.target && it.target !== it.name ? " · " + it.target : ""), desc: "", item: it.label, ref: it });
});
m.nodes.forEach(function (n) {
out.push({ kind: n.kind, label: n.label, meta: n.kind + " · " + n.item, desc: n.desc, item: n.item, ref: n, qualified: qualified(n) });
});
md.columns.forEach(function (list, id) {
var owner = m.byIdentity.get(id);
list.forEach(function (c) {
out.push({ kind: "Column", label: c.column, meta: "Column · " + (owner ? owner.label : c.schema + "." + c.object) + " · " + c.item, desc: c.description || "", item: c.item, ref: c, owner: owner });
});
});
md.models.forEach(function (mo) {
mo.tables.forEach(function (tb) {
out.push({ kind: "Semantic table", label: tb.name, meta: "Semantic table · " + mo.name, desc: tb.description || "", item: mo.item, ref: tb });
tb.columns.forEach(function (c) {
out.push({ kind: "Semantic column", label: c.column, meta: "Semantic column · " + tb.name + " · " + mo.name, desc: c.description || "", item: mo.item, ref: c, table: tb });
});
tb.measures.forEach(function (c) {
out.push({ kind: "Measure", label: c.measure, meta: "Measure · " + tb.name + " · " + mo.name, desc: c.description || "", item: mo.item, ref: c, table: tb });
});
});
});
out.forEach(function (e) {
e.lower = e.label.toLowerCase(); e.descLower = e.desc.toLowerCase(); e.metaLower = e.meta.toLowerCase();
e.nameLower = e.ref && e.ref.key && e.ref.object ? e.ref.object.toLowerCase() : e.lower;
});
m.entries = out;
return out;
}
function searchEntries(entries, query, kind) {
var terms = String(query || "").toLowerCase().split(/\s+/).filter(Boolean), found = [];
entries.forEach(function (e) {
if (kind && kind !== "All" && e.kind !== kind) return;
var score = 0;
for (var i = 0; i < terms.length; i++) {
var term = terms[i], s = 0, w = wildcard(term);
if (w) s = w.test(e.lower) || w.test(e.nameLower) ? 70 : 0;
else if (e.lower === term || e.nameLower === term) s = 100;
else if (e.lower.indexOf(term) === 0 || e.nameLower.indexOf(term) === 0) s = 80;
else if ((" " + e.lower.replace(/[._/\-]/g, " ")).indexOf(" " + term) >= 0) s = 60;
else if (e.lower.indexOf(term) >= 0) s = 40;
else if (e.metaLower.indexOf(term) >= 0) s = 20;
else if (e.descLower.indexOf(term) >= 0) s = 10;
if (!s) return;
score += s;
}
found.push({ e: e, score: terms.length ? score : 0 });
});
found.sort(function (a, b) {
return b.score - a.score || entryRank(a.e) - entryRank(b.e) || compare(a.e.label, b.e.label) || compare(a.e.meta, b.e.meta);
});
return found.map(function (f) { return f.e; });
}
var ENTRY_RANK = { "Item": 0, "Semantic table": 2, "Column": 3, "Semantic column": 3, "Measure": 3 };
function entryRank(e) { return e.kind in ENTRY_RANK ? ENTRY_RANK[e.kind] : 1; }
var ENTITY_KINDS = ["All", "Item", "Table", "View", "Folder", "Shortcut", "Test", "Assumption", "Column"];
var SEMANTIC_TYPES = ["SemanticModel", "Report"];
/* The meaning of the landed and curated data: the declared relationships
between Lakehouse and Warehouse objects, and their dictionary. The Semantic
model page is its counterpart for models. */
function entitiesPage(body, m) {
var s = pageState("entities"), md = metadata(m);
s.item = s.item || "all"; s.kind = s.kind || "All"; s.query = s.query || ""; s.er = s.er || {};
var items = visibleItems(m).filter(function (it) { return SEMANTIC_TYPES.indexOf(it.type) < 0 && (it.nodes.length || it.target); })
.sort(function (a, b) { return typeRank(a.type) - typeRank(b.type) || compare(a.name, b.name); });
if (s.item !== "all" && !items.some(function (it) { return it.label === s.item; })) s.item = "all";
var entries = dictionaryEntries(m).filter(function (e) {
return ENTITY_KINDS.indexOf(e.kind) > 0 && SEMANTIC_TYPES.indexOf(itemType(e.item)) < 0 && (s.item === "all" || e.item === s.item);
});
var counts = {};
entries.forEach(function (e) { counts[e.kind] = (counts[e.kind] || 0) + 1; });
var picker = el("select", { "class": "wd-select", "aria-label": "Item", onchange: function () {
s.item = this.value; s.selected = null; s.er = { up: s.er.up, down: s.er.down, maximised: s.er.maximised }; saveState(); redraw();
} }, [el("option", { value: "all", text: "Every Lakehouse and Warehouse" })].concat(items.map(function (it) {
return el("option", { value: it.label, selected: it.label === s.item ? "selected" : null, text: it.type + " · " + it.name });
})));
var search = searchBox({
placeholder: "Search " + fmt(entries.length) + " tables, views, folders and columns · * matches any text · Shift adds",
find: function (q) {
return q.trim() ? searchEntries(entries, q, "All").slice(0, 12).map(function (e) { return { kind: e.kind, label: e.label, meta: e.meta, desc: e.desc, entry: e }; }) : [];
},
onPick: function (r, adding) { choose(r.entry, adding); },
onPattern: function (q) { er.addPattern(q); }
});
var er = erWorkspace(body, m, s.er, { item: s.item, tools: [search, picker], describe: renderSide,
matches: function (q) { return searchEntries(entries, q, "All").filter(function (e) { return e.ref && e.ref.key; }).map(function (e) { return e.ref.id; }); },
onPick: function (id) {
var entry = tableEntry(id);
s.selected = entry ? entryId(entry) : null;
renderSide(); renderList(); renderDetail();
saveState();
} });
var facets = el("div", { "class": "wd-facets", role: "radiogroup", "aria-label": "Entry kind" });
var input = el("input", { "class": "wd-search wd-search-wide", type: "search", value: s.query, placeholder: "Filter " + fmt(entries.length) + " entries by name, kind or description · * matches any text", "aria-label": "Filter the dictionary", autocomplete: "off", spellcheck: "false" });
var list = el("div", { "class": "wd-entry-list", role: "listbox" }), detail = el("div", { "class": "wd-entry-detail" }), note = el("div", { "class": "wd-status-line" });
body.appendChild(section("Dictionary", [el("div", { "class": "wd-toolbar" }, [input]), facets, note, el("div", { "class": "wd-dictionary" }, [list, detail])]));
function tableEntry(id) { return entries.filter(function (e) { return e.ref && e.ref.key && e.ref.id === id; })[0] || null; }
function tableOf(e) {
if (e.ref && e.ref.key) return e.ref.id;
if (e.kind === "Column") return identityKey(e.ref.item, e.ref.schema, e.ref.object);
return null;
}
function current() { return entries.filter(function (e) { return entryId(e) === s.selected; })[0] || null; }
function renderFacets() {
facets.textContent = "";
ENTITY_KINDS.forEach(function (k) {
if (k !== "All" && !counts[k]) return;
facets.appendChild(el("button", { type: "button", role: "radio", "class": "wd-facet", "aria-checked": String(s.kind === k),
onclick: function () { s.kind = k; renderFacets(); renderList(); saveState(); } },
[k === "All" ? null : kindMark(k), k + " ", el("span", { "class": "wd-facet-count", text: fmt(k === "All" ? entries.length : counts[k]) })]));
});
}
function renderList() {
var found = searchEntries(entries, s.query, s.kind), shown = found.slice(0, 100);
list.textContent = "";
note.textContent = found.length > 100 ? "Showing the first 100 of " + fmt(found.length) + " matches. Refine the filter to narrow them." : fmt(found.length) + (found.length === 1 ? " match" : " matches");
shown.forEach(function (e) {
list.appendChild(el("button", { type: "button", role: "option", "class": "wd-entry", "aria-selected": String(s.selected === entryId(e)),
onclick: function () { choose(e, false); } }, [
el("span", { "class": "wd-entry-label" }, [kindMark(e.kind), e.label]),
el("span", { "class": "wd-entry-meta", text: e.meta }),
e.desc ? el("span", { "class": "wd-entry-desc", text: e.desc }) : null
]));
});
if (!shown.length) list.appendChild(empty("Nothing matches. Try fewer words, or another kind."));
}
/* An entry chosen anywhere on the page shows in both details panels, and its
table in the diagram when the table has relationships. */
function choose(e, adding) {
s.selected = entryId(e);
var id = tableOf(e);
if (id && er.has(id)) er.select(id, adding);
else if (id) er.say(e.label + " is not a declared table" + (s.item !== "all" ? " in " + itemName(s.item) : ""));
renderSide(); renderList(); renderDetail();
saveState();
}
function renderSide(panel) {
panel = panel || er.side;
var e = current();
if (e) entryDetail(panel, m, md, e, function (other) { choose(other, false); });
else { panel.textContent = ""; panel.appendChild(empty("Search for a table, or select one in the diagram, to see its definition, keys and columns.")); }
}
function renderDetail() {
var e = current();
if (e) entryDetail(detail, m, md, e, function (other) { choose(other, false); });
else { detail.textContent = ""; detail.appendChild(empty("Select an entry to see its definition, keys, columns and lineage.")); }
}
input.addEventListener("input", function () { s.query = input.value; renderList(); saveState(); });
renderFacets(); renderList(); renderDetail();
}
function entryId(e) {
if (e.kind === "Item") return "item|" + e.item;
if (e.ref && e.ref.key) return "node|" + e.ref.key;
if (e.kind === "Column") return "col|" + identityKey(e.ref.item, e.ref.schema, e.ref.object) + "|" + e.ref.column;
if (e.kind === "Semantic table") return "smt|" + e.item + "|" + e.ref.name;
return e.kind + "|" + e.item + "|" + (e.table ? e.table.name : "") + "|" + e.label;
}
function entryDetail(panel, m, md, e, select) {
panel.textContent = "";
var entries = dictionaryEntries(m);
function find(kind, test) { return entries.filter(function (x) { return x.kind === kind && test(x); })[0]; }
function openNode(key) {
var x = entries.filter(function (y) { return y.ref && y.ref.key === key; })[0];
if (x) select(x);
}
if (e.kind === "Item") {
var it = e.ref;
panel.appendChild(el("div", { "class": "wd-eyebrow", text: it.type }));
panel.appendChild(el("h2", { "class": "wd-detail-title", text: it.name }));
var facts = el("dl", { "class": "wd-facts" });
[["Fabric item", it.target], ["Workspace", it.workspace], ["Weaver version", it.version], ["Objects", fmt(it.nodes.length)]].forEach(function (f) {
if (f[1]) { facts.appendChild(el("dt", { text: f[0] })); facts.appendChild(el("dd", { text: f[1] })); }
});
panel.appendChild(facts);
var schemas = md.schemas.filter(function (r) { return r.item === it.label; });
if (schemas.length) {
panel.appendChild(el("h3", { "class": "wd-h3", text: "Schemas" }));
panel.appendChild(el("dl", { "class": "wd-columns" }, schemas.reduce(function (a, r) { return a.concat([el("dt", { text: r.schema }), el("dd", { text: r.description || "" })]); }, [])));
}
panel.appendChild(el("h3", { "class": "wd-h3", text: "Objects" }));
panel.appendChild(el("ul", { "class": "wd-list" }, it.nodes.slice(0, 200).map(function (n) { return el("li", {}, [nodeLink(m, n.key, openNode)]); })));
return;
}
if (e.ref && e.ref.key) {
var n = e.ref;
details(panel, m, n.key, { onOpen: openNode, columns: md.columns });
var declared = md.tables.get(n.id) || md.folders.get(n.id), validation = md.validations.get(n.id);
if (declared) {
var facts2 = el("dl", { "class": "wd-facts" });
[["Primary key", declared.primarykey], ["Not null", declared.notnull], ["Identity column", declared.identity], ["File key", declared.filekey],
["Incremental", declared.incremental ? "Yes" : null], ["Prohibit rebuild", declared.prohibitrebuild ? "Yes" : null]].forEach(function (f) {
if (f[1]) { facts2.appendChild(el("dt", { text: f[0] })); facts2.appendChild(el("dd", { "class": "wd-mono", text: f[1] })); }
});
panel.insertBefore(facts2, panel.querySelector(".wd-h3"));
if (declared.lineage) panel.insertBefore(el("p", { "class": "wd-lineage-text" }, [el("b", { text: "Lineage. " }), declared.lineage]), facts2.nextSibling);
}
if (validation && validation.primarykey) panel.appendChild(el("p", { "class": "wd-muted", text: "Correlation key: " + validation.primarykey }));
var keys = md.keys.get(n.id) || [], refs = md.references.get(n.id) || [], back = md.referencedBy.get(n.id) || [];
if (keys.length || refs.length || back.length) {
panel.appendChild(el("h3", { "class": "wd-h3", text: "Keys and relationships" }));
panel.appendChild(el("ul", { "class": "wd-list wd-mono" }, keys.map(function (k) { return el("li", { text: k.type + " (" + k.columns + ")" }); })
.concat(refs.map(function (r) { return el("li", { text: "(" + r.fromColumns.join(", ") + ") → " + r.to.split("|").slice(1).join(".") + " (" + r.toColumns.join(", ") + ")" }); }))
.concat(back.map(function (r) { return el("li", { text: r.from.split("|").slice(1).join(".") + " (" + r.fromColumns.join(", ") + ") → (" + r.toColumns.join(", ") + ")" }); }))));
}
if (n.kind === KIND.MODEL) {
var mo = md.models.get(n.item);
if (mo) semanticSummary(panel, m, mo, function (tb) { var x = find("Semantic table", function (y) { return y.ref === tb; }); if (x) select(x); });
}
return;
}
if (e.kind === "Column") {
panel.appendChild(el("div", { "class": "wd-eyebrow", text: "Declared column" }));
panel.appendChild(el("h2", { "class": "wd-detail-title", text: e.ref.column }));
panel.appendChild(el("p", { "class": e.ref.description ? "wd-desc" : "wd-desc wd-muted", text: e.ref.description || "No description is declared." }));
if (e.ref.identity) panel.appendChild(el("p", { "class": "wd-muted", text: "Weaver's managed surrogate column." }));
if (e.owner) panel.appendChild(el("p", {}, ["Of ", nodeLink(m, e.owner.key, openNode)]));
panel.appendChild(el("p", { "class": "wd-note", text: "The dictionary describes declared columns; it does not inventory every physical column." }));
return;
}
var tb = e.kind === "Semantic table" ? e.ref : e.table;
if (e.kind === "Semantic column" || e.kind === "Measure") {
panel.appendChild(el("div", { "class": "wd-eyebrow", text: e.kind }));
panel.appendChild(el("h2", { "class": "wd-detail-title", text: e.label }));
panel.appendChild(el("div", { "class": "wd-muted", text: tb.name + " · " + tb.model.name }));
panel.appendChild(el("p", { "class": e.ref.description ? "wd-desc" : "wd-desc wd-muted", text: e.ref.description || "No description." }));
var f3 = el("dl", { "class": "wd-facts" });
[["Data type", e.ref.datatype], ["Kind", e.ref.columntype], ["Source column", e.ref.sourcecolumn], ["Format", e.ref.format]].forEach(function (f) {
if (f[1]) { f3.appendChild(el("dt", { text: f[0] })); f3.appendChild(el("dd", { text: f[1] })); }
});
panel.appendChild(f3);
if (e.ref.expression) panel.appendChild(el("pre", { "class": "wd-code", text: e.ref.expression }));
return;
}
semanticTableDetail(panel, m, tb, openNode);
}
function modelList(m) {
return Array.from(metadata(m).models.values()).sort(function (a, b) { return compare(a.name, b.name); });
}
function semanticSummary(panel, m, mo, onTable) {
panel.appendChild(el("h3", { "class": "wd-h3", text: "Tables · " + mo.tables.size }));
panel.appendChild(el("ul", { "class": "wd-list" }, modelTables(mo, "authored").map(function (tb) {
return el("li", {}, [el("button", { "class": "wd-link", type: "button", onclick: function () { onTable(tb); } }, [kindMark("Semantic table"), tb.name]),
el("span", { "class": "wd-grow" }), el("span", { "class": "wd-muted", text: tb.mode || "" })]);
})));
}
function semanticTableDetail(panel, m, tb, openNode) {
panel.appendChild(el("div", { "class": "wd-eyebrow" }, [kindMark("Semantic table"), " Semantic table"]));
panel.appendChild(el("h2", { "class": "wd-detail-title", text: tb.name }));
panel.appendChild(el("div", { "class": "wd-muted", text: tb.model.name + (tb.ordinal !== null ? " · table " + tb.ordinal + " in authored order" : "") }));
panel.appendChild(el("p", { "class": tb.description ? "wd-desc" : "wd-desc wd-muted", text: tb.description || "No description." }));
var facts = el("dl", { "class": "wd-facts" });
[["Storage mode", tb.mode], ["Source access", tb.access]].forEach(function (f) {
if (f[1]) { facts.appendChild(el("dt", { text: f[0] })); facts.appendChild(el("dd", { text: f[1] })); }
});
panel.appendChild(facts);
if (tb.sources.length) {
panel.appendChild(el("h3", { "class": "wd-h3", text: "Reads" }));
panel.appendChild(el("ul", { "class": "wd-list" }, tb.sources.map(function (src) {
return el("li", {}, [src.node && openNode ? nodeLink(m, src.node.key, openNode) : el("span", { "class": "wd-mono", text: src.reference })]);
})));
}
var rels = tb.model.relationships.filter(function (r) { return r.from === tb.name || r.to === tb.name; });
if (rels.length) {
panel.appendChild(el("h3", { "class": "wd-h3", text: "Relationships · " + rels.length }));
panel.appendChild(el("ul", { "class": "wd-list wd-mono" }, rels.map(relationshipLine)));
}
if (tb.columns.length) {
panel.appendChild(el("h3", { "class": "wd-h3", text: "Columns · " + tb.columns.length }));
panel.appendChild(dataTable([
{ key: "column", title: "Column", value: function (c) { return c.column; } },
{ key: "datatype", title: "Type", value: function (c) { return c.datatype || ""; } },
{ key: "description", title: "Description", value: function (c) { return c.description || ""; } }
], tb.columns, { limit: 300, sort: null }));
}
if (tb.measures.length) {
panel.appendChild(el("h3", { "class": "wd-h3", text: "Measures · " + tb.measures.length }));
tb.measures.forEach(function (ms) {
panel.appendChild(el("details", { "class": "wd-measure" }, [
el("summary", {}, [el("b", { text: ms.measure }), ms.description ? el("span", { "class": "wd-muted", text: " · " + ms.description }) : null]),
ms.expression ? el("pre", { "class": "wd-code", text: ms.expression }) : null,
ms.format ? el("div", { "class": "wd-muted", text: "Format " + ms.format }) : null
]));
});
}
}
function relationshipLine(r) {
return el("li", { "class": r.active ? null : "wd-inactive" }, [
r.from + "[" + (r.fromColumn || "") + "]  " + notation({ r: r, factIsFrom: true }, true) + "  " + r.to + "[" + (r.toColumn || "") + "]" + (r.active ? "" : "  inactive")
]);
}
/* ---- bus matrix -------------------------------------------------------------- */
/* Fact-side tables against dimension-side tables, from a model's direct
relationships. The one side of a one-to-many relationship is a dimension and
its many side a fact. A one-to-one or many-to-many relationship takes the
roles its tables already have, or its from and to tables when they have none;
it is listed apart only when both its tables are on the same side. */
function busMatrix(mo) {
var facts = new Map(), dims = new Map(), cells = new Map(), other = [], later = [];
function place(fact, dim, r) {
facts.set(fact, true); dims.set(dim, true);
var key = fact + "\u0001" + dim, cell = cells.get(key);
if (!cell) cells.set(key, cell = { active: 0, inactive: 0, relationships: [] });
cell[r.active ? "active" : "inactive"] += 1;
cell.relationships.push({ r: r, factIsFrom: r.from === fact });
}
mo.relationships.forEach(function (r) {
if (r.fromCardinality === "many" && r.toCardinality === "one") place(r.from, r.to, r);
else if (r.fromCardinality === "one" && r.toCardinality === "many") place(r.to, r.from, r);
else later.push(r);
});
function canBeFact(name) { return facts.has(name) || !dims.has(name); }
function canBeDim(name) { return dims.has(name) || !facts.has(name); }
later.forEach(function (r) {
if (canBeFact(r.from) && canBeDim(r.to)) place(r.from, r.to, r);
else if (canBeFact(r.to) && canBeDim(r.from)) place(r.to, r.from, r);
else other.push(r);
});
var related = new Set();
mo.relationships.forEach(function (r) { related.add(r.from); related.add(r.to); });
var isolated = Array.from(mo.tables.keys()).filter(function (name) { return !related.has(name); });
return { facts: facts, dims: dims, cells: cells, other: other, isolated: isolated, notation: notation,
mixed: Array.from(facts.keys()).filter(function (name) { return dims.has(name); }) };
}
/* A relationship as the matrix writes it, read from the row table to the
column table: each side's cardinality, and the arrow the filter travels. */
function notation(entry, rowIsFact) {
var r = entry.r, rowIsFrom = entry.factIsFrom === rowIsFact, row = rowIsFrom ? r.from : r.to;
var card = function (c) { return c === "many" ? "*" : "1"; };
var left = card(rowIsFrom ? r.fromCardinality : r.toCardinality), right = card(rowIsFrom ? r.toCardinality : r.fromCardinality);
var filtered = r.fromCardinality !== r.toCardinality ? (r.fromCardinality === "many" ? r.from : r.to) : r.from;
var arrow = /both/i.test(r.crossFilter || "") ? "↔" : filtered === row ? "←" : "→";
return left + " " + arrow + " " + right;
}
/* The fact × dimension matrix of one model, read from row to column. */
function busMatrixView(mo, s) {
var host = el("div"), bus = busMatrix(mo), order = modelTables(mo, s.order).map(function (tb) { return tb.name; });
function sorted(map) { return order.filter(function (n) { return map.has(n); }).concat(Array.from(map.keys()).filter(function (n) { return order.indexOf(n) < 0; }).sort(compare)); }
var factsAreRows = s.dims === "columns";
var rows = sorted(factsAreRows ? bus.facts : bus.dims), cols = sorted(factsAreRows ? bus.dims : bus.facts);
if (!rows.length) { host.appendChild(empty("This model records no relationship.")); }
else {
var mixedMark = function (name) { return bus.mixed.indexOf(name) >= 0 ? el("i", { "class": "wd-bus-mixed", title: "On the fact side of one relationship and the dimension side of another", text: " ◐" }) : null; };
host.appendChild(el("div", { "class": "wd-table-wrap wd-bus-wrap" }, [el("table", { "class": "wd-bus" }, [
el("thead", {}, [el("tr", {}, [el("th", { "class": "wd-bus-corner", text: factsAreRows ? "Fact ↓   Dimension →" : "Dimension ↓   Fact →" })].concat(cols.map(function (c) {
return el("th", { scope: "col", "class": "wd-bus-dim" }, [el("span", {}, [c, mixedMark(c)])]);
})))]),
el("tbody", {}, rows.map(function (row) {
return el("tr", {}, [el("th", { scope: "row" }, [row, mixedMark(row)])].concat(cols.map(function (col) {
var cell = bus.cells.get(factsAreRows ? row + "\u0001" + col : col + "\u0001" + row);
if (!cell) return el("td", { "class": "wd-bus-empty" });
var shown = cell.relationships.filter(function (e) { return e.r.active; })[0] || cell.relationships[0], count = cell.relationships.length;
return el("td", { "class": "wd-bus-cell" + (cell.active ? "" : " wd-bus-inactive"),
title: cell.relationships.map(function (e) { return notation(e, factsAreRows) + "  " + e.r.from + "[" + e.r.fromColumn + "] → " + e.r.to + "[" + e.r.toColumn + "]" + (e.r.active ? "" : " (inactive)"); }).join("\n") },
[notation(shown, factsAreRows), count > 1 ? el("sup", { text: String(count) }) : null]);
})));
}))
])]));
host.appendChild(el("div", { "class": "wd-legend" }, [
el("span", { "class": "wd-key", text: "* ← 1  many to one" }), el("span", { "class": "wd-key", text: "* ← *  many to many" }),
el("span", { "class": "wd-key", text: "↔  filters both ways" }), el("span", { "class": "wd-key wd-muted", text: "grey: inactive only" }),
el("span", { "class": "wd-key", text: "²  relationships between the pair" }), el("span", { "class": "wd-key", text: "◐ on both sides" }),
el("span", { "class": "wd-key", text: "Read from the row table to the column table. Cells show direct relationships, not filter propagation; an empty cell records none." })
]));
}
if (bus.other.length) {
host.appendChild(el("h3", { "class": "wd-h3", text: "Between two tables on the same side · " + bus.other.length }));
host.appendChild(el("ul", { "class": "wd-list wd-mono" }, bus.other.map(relationshipLine)));
}
if (bus.isolated.length) {
host.appendChild(el("h3", { "class": "wd-h3", text: "Tables with no relationship · " + bus.isolated.length }));
host.appendChild(el("p", { "class": "wd-muted", text: order.filter(function (n) { return bus.isolated.indexOf(n) >= 0; }).join(", ") }));
}
if (mo.relationships.length) {
host.appendChild(el("details", { "class": "wd-more-detail" }, [el("summary", { text: "Every relationship · " + mo.relationships.length }),
el("ul", { "class": "wd-list wd-mono" }, mo.relationships.slice().sort(function (a, b) { return compare(a.from, b.from) || compare(a.to, b.to); }).map(relationshipLine))]));
}
return host;
}
/* One model, chosen at the top: what it is, how its tables relate, its tables,
columns and measures, and the managed sources they read. The Entity
dictionary page is its counterpart for Lakehouses and Warehouses. */
function semanticPage(body, m) {
var s = pageState("semantic"), models = modelList(m);
s.order = s.order || "authored"; s.dims = s.dims || "columns"; s.query = s.query || "";
if (!models.length) { body.appendChild(empty("No semantic model is recorded in the catalogue.")); return; }
if (!s.model || !models.some(function (mo) { return mo.item === s.model; })) s.model = models[0].item;
var mo = metadata(m).models.get(s.model);
var picker = el("select", { "class": "wd-select wd-select-strong", "aria-label": "Semantic model", onchange: function () { s.model = this.value; s.table = null; saveState(); redraw(); } },
models.map(function (x) { return el("option", { value: x.item, selected: x.item === s.model ? "selected" : null, text: x.name }); }));
var input = el("input", { "class": "wd-search", type: "search", value: s.query, placeholder: "Search this model's tables, columns and measures", "aria-label": "Search the model", autocomplete: "off", spellcheck: "false" });
body.appendChild(el("div", { "class": "wd-toolbar" }, [picker, el("div", { "class": "wd-searchbox" }, [input])]));
var refresh = mo.node ? effectiveLoad(mo.node) : null, it = m.items.get(mo.item), measureCount = 0, columnCount = 0;
mo.tables.forEach(function (tb) { measureCount += tb.measures.length; columnCount += tb.columns.length; });
var facts = el("dl", { "class": "wd-facts wd-facts-wide" });
function fact(label, value) { facts.appendChild(el("dt", { text: label })); facts.appendChild(el("dd", {}, [value])); }
fact("Last refresh", refresh ? el("span", {}, [chip(refresh.result), " " + stamp(refresh.completed)]) : el("span", { "class": "wd-muted", text: "Nothing has been processed since it was built" }));
if (mo.node && mo.node.built) fact("Built", stamp(mo.node.built));
if (it && it.target) fact("Fabric item", it.target);
fact("Contents", fmt(mo.tables.size) + " tables · " + fmt(columnCount) + " columns · " + fmt(measureCount) + " measures · " + fmt(mo.relationships.length) + " relationships");
var validations = it ? it.nodes.filter(isValidation) : [];
body.appendChild(el("div", { "class": "wd-model-head" }, [
el("div", {}, [el("div", { "class": "wd-eyebrow", text: "Semantic model" }), el("h2", { "class": "wd-detail-title", text: mo.name }),
el("p", { "class": mo.description ? "wd-desc" : "wd-desc wd-muted", text: mo.description || "No description." }), facts]),
validations.length ? el("div", {}, [el("h3", { "class": "wd-h3", text: "Tests and Assumptions · " + validations.length }),
el("ul", { "class": "wd-list" }, validations.map(function (v) {
return el("li", {}, [kindMark(v.kind), v.label, el("span", { "class": "wd-grow" }), chip(v.test ? v.test.result : null, v.test ? null : "Not run"),
v.test && v.test.failures ? el("span", { "class": "wd-muted", text: " " + fmt(v.test.failures) + " rows" }) : null]);
}))]) : null
]));
var busHost = el("div");
function renderBus() { busHost.textContent = ""; busHost.appendChild(busMatrixView(mo, s)); }
body.appendChild(section("Relationships", [el("div", { "class": "wd-toolbar" }, [
segmented("Dimensions", ["columns", "rows"], s.dims, function (v) { s.dims = v; renderBus(); saveState(); }, function (v) { return v === "columns" ? "Columns" : "Rows"; }),
segmented("Order", ["authored", "alphabetical"], s.order, function (v) { s.order = v; renderBus(); renderTables(); saveState(); }, function (v) { return v === "authored" ? "Authored" : "A–Z"; })
]), busHost]));
var tablesHost = el("div"), detail = el("div", { "class": "wd-entry-detail" }), measuresHost = el("div");
function matches(text) { var q = s.query.toLowerCase().trim(); return !q || String(text || "").toLowerCase().indexOf(q) >= 0; }
function tableMatches(tb) {
return matches(tb.name) || matches(tb.description) || tb.columns.some(function (c) { return matches(c.column) || matches(c.description); }) ||
tb.measures.some(function (x) { return matches(x.measure) || matches(x.description); });
}
function renderTables() {
tablesHost.textContent = "";
var tables = modelTables(mo, s.order).filter(tableMatches);
if (s.order === "authored" && tables.some(function (tb) { return tb.ordinal === null; })) {
tablesHost.appendChild(el("p", { "class": "wd-note", text: "This model was read back without an authored table order, so its tables are listed alphabetically. Build it again to record the order." }));
}
tablesHost.appendChild(dataTable([
{ key: "ordinal", title: "#", value: function (tb) { return tb.ordinal; }, numeric: true, sortable: false },
{ key: "name", title: "Table", value: function (tb) { return tb.name; }, sortable: false },
{ key: "mode", title: "Mode", value: function (tb) { return tb.mode || ""; }, sortable: false },
{ key: "columns", title: "Columns", value: function (tb) { return tb.columns.length; }, numeric: true, sortable: false },
{ key: "measures", title: "Measures", value: function (tb) { return tb.measures.length; }, numeric: true, sortable: false },
{ key: "reads", title: "Reads", value: function (tb) { return tb.sources.map(function (src) { return src.node ? src.node.label : src.reference; }).join(", "); }, sortable: false }
], tables, { limit: 500, onRow: function (tb) { s.table = tb.name; showTable(tb); saveState(); }, emptyText: "No table matches." }));
}
function showTable(tb) { detail.textContent = ""; semanticTableDetail(detail, m, tb, null); }
body.appendChild(section("Tables", [el("div", { "class": "wd-semantic-grid" }, [tablesHost, detail])]));
var chosen = s.table && mo.tables.get(s.table);
if (chosen) showTable(chosen); else detail.appendChild(empty("Select a table to see its columns, measures and relationships."));
function renderMeasures() {
measuresHost.textContent = "";
var all = [];
mo.tables.forEach(function (tb) { tb.measures.forEach(function (x) { if (matches(x.measure) || matches(x.description) || matches(tb.name)) all.push({ table: tb.name, x: x }); }); });
if (!all.length) { measuresHost.appendChild(empty(measureCount ? "No measure matches." : "This model has no measures.")); return; }
all.sort(function (a, b) { return compare(a.x.measure, b.x.measure); });
measuresHost.appendChild(el("div", { "class": "wd-measures" }, all.map(function (e) {
return el("details", { "class": "wd-measure" }, [
el("summary", {}, [el("b", { text: e.x.measure }), el("span", { "class": "wd-muted", text: " · " + e.table }),
e.x.description ? el("span", { "class": "wd-measure-desc", text: e.x.description }) : null]),
e.x.expression ? el("pre", { "class": "wd-code", text: e.x.expression }) : null,
e.x.format ? el("div", { "class": "wd-muted", text: "Format " + e.x.format }) : null
]);
})));
}
body.appendChild(section("Measures · " + fmt(measureCount), [measuresHost]));
body.appendChild(section("Sources", [sourceReuse(m, models, false, mo.item)]));
input.addEventListener("input", function () { s.query = input.value; renderTables(); renderMeasures(); });
renderBus(); renderTables(); renderMeasures();
}
/* Logical sources against the models whose tables read them. */
function sourceReuse(m, models, modelsAsRows, only) {
var sources = new Map();
models.forEach(function (mo) {
mo.tables.forEach(function (tb) {
tb.sources.forEach(function (src) {
var key = src.node ? src.node.key : src.reference, entry = sources.get(key);
if (!entry) sources.set(key, entry = { label: src.node ? src.node.label : src.reference, item: src.item || "", by: new Map() });
addTo(entry.by, mo.item, tb.name);
});
});
});
if (!sources.size) return empty("No semantic table records a managed source.");
var list = Array.from(sources.values()).filter(function (src) { return !only || src.by.has(only); })
.sort(function (a, b) { return compare(a.item, b.item) || compare(a.label, b.label); });
if (!list.length) return empty("No table of this model records a managed source.");
var rows = modelsAsRows ? models : list, cols = modelsAsRows ? list : models;
function name(x) { return x.name !== undefined ? [x.name] : [x.label, el("span", { "class": "wd-muted", text: " " + itemName(x.item) })]; }
function tables(row, col) { var src = modelsAsRows ? col : row, mo = modelsAsRows ? row : col; return src.by.get(mo.item); }
return el("div", { "class": "wd-table-wrap wd-bus-wrap" }, [el("table", { "class": "wd-bus" }, [
el("thead", {}, [el("tr", {}, [el("th", { "class": "wd-bus-corner", text: modelsAsRows ? "Model ↓   Source →" : "Source ↓   Model →" })].concat(cols.map(function (c) {
return el("th", { scope: "col", "class": "wd-bus-dim" }, [el("span", {}, name(c))]);
})))]),
el("tbody", {}, rows.map(function (row) {
return el("tr", {}, [el("th", { scope: "row" }, name(row))].concat(cols.map(function (col) {
var found = tables(row, col);
return found ? el("td", { "class": "wd-bus-cell", title: found.join(", ") }, [found.length > 1 ? String(found.length) : "✓"]) : el("td", { "class": "wd-bus-empty" });
})));
}))
])]);
}
var ER = { NODES: 80, EXPANDED: 120, WRAP: 8, BOX: 220, HEAD: 34, ROW: 18, GAP_X: 64, GAP_ROW: 120, COLUMNS: 8 };
/* The declared tables and relationships of the Lakehouses and Warehouses, or
of one of them: a relationship belongs to an item when either end is in it.
A table with no relationship is a node of its own. Both ends of a
relationship keep their foreign and primary columns. */
function erGraph(m, item) {
var md = metadata(m), nodes = new Map(), edges = [];
function node(id) {
if (nodes.has(id)) return;
var parts = id.split("|"), owner = m.byIdentity.get(id) || null, declared = md.tables.get(id);
var keys = declared && declared.primarykey ? [{ type: "Primary key", columns: splitList(declared.primarykey) }] : [];
nodes.set(id, { id: id, label: owner ? owner.label : parts[1] + "." + parts[2], item: parts[0],
columns: (md.columns.get(id) || []).map(function (c) { return c.column; }),
keys: keys.concat((md.keys.get(id) || []).map(function (k) { return { type: k.type, columns: splitList(k.columns) }; })),
owner: owner, refs: [], back: [] });
}
md.foreignKeys.forEach(function (fk) {
if (item && item !== "all" && fk.from.split("|")[0] !== item && fk.to.split("|")[0] !== item) return;
node(fk.from); node(fk.to);
edges.push({ from: fk.from, to: fk.to, fromColumns: fk.fromColumns, toColumns: fk.toColumns, label: "", active: true, many: true });
});
md.tables.forEach(function (_, id) { if (!item || item === "all" || id.split("|")[0] === item) node(id); });
edges.forEach(function (e, i) { e.id = i; nodes.get(e.from).refs.push(e); nodes.get(e.to).back.push(e); });
return { nodes: nodes, edges: edges };
}
function parentsOf(n) { return n.refs.map(function (e) { return e.to; }); }
function childrenOf(n) { return n.back.map(function (e) { return e.from; }); }
/* The selected tables with their parents to depth up and their children to
depth down, nearest first up to ER.NODES, plus what the reader has expanded.
rank orders the rows: parents above, children below. With nothing selected
the window is the whole graph, or its ER.NODES most related tables, ranked
by each table's longest chain of references. Every related table left out
is counted on the shown table it hangs from. */
function erWindow(g, selection, up, down, expanded) {
var seeds = (Array.isArray(selection) ? selection : [selection]).filter(function (id) { return g.nodes.has(id); });
var rank = new Map(), reach = g.nodes.size;
if (seeds.length) {
seeds.forEach(function (id) { rank.set(id, 0); });
[[parentsOf, -1, up], [childrenOf, 1, down]].forEach(function (w) {
var limit = w[2] < 0 ? Infinity : w[2], frontier = seeds.slice();
for (var step = 1; step <= limit && frontier.length; step++) {
var found = [];
frontier.forEach(function (id) {
w[0](g.nodes.get(id)).forEach(function (j) { if (!rank.has(j)) { rank.set(j, w[1] * step); found.push(j); } });
});
frontier = found;
}
});
reach = rank.size;
var ranked = Array.from(rank, function (x) { return { id: x[0], d: x[1] }; }).sort(function (a, b) {
return Math.abs(a.d) - Math.abs(b.d) || a.d - b.d || compare(g.nodes.get(a.id).label, g.nodes.get(b.id).label) || compare(a.id, b.id);
});
rank = new Map(ranked.slice(0, ER.NODES).map(function (r) { return [r.id, r.d]; }));
} else {
var most = Array.from(g.nodes.values()).sort(function (a, b) {
return b.refs.length + b.back.length - a.refs.length - a.back.length || compare(a.label, b.label) || compare(a.id, b.id);
}).slice(0, ER.NODES), inside = new Set(most.map(function (n) { return n.id; }));
var visiting = new Set();
var level = function (id) {
if (rank.has(id)) return rank.get(id);
if (visiting.has(id)) return 0;
visiting.add(id);
var deepest = -1;
parentsOf(g.nodes.get(id)).forEach(function (p) { if (p !== id && inside.has(p)) deepest = Math.max(deepest, level(p)); });
visiting.delete(id);
rank.set(id, deepest + 1);
return deepest + 1;
};
inside.forEach(level);
}
var kept = rank.size, added = new Set();
(expanded || []).forEach(function (id) {
if (!g.nodes.has(id) || rank.has(id) || added.size >= ER.EXPANDED) return;
var n = g.nodes.get(id), at = null;
childrenOf(n).forEach(function (c) { if (rank.has(c)) at = at === null ? rank.get(c) - 1 : Math.min(at, rank.get(c) - 1); });
if (at === null) parentsOf(n).forEach(function (p) { if (rank.has(p)) at = at === null ? rank.get(p) + 1 : Math.max(at, rank.get(p) + 1); });
if (at === null) return;
rank.set(id, at); added.add(id);
});
var more = new Map(), hidden = new Set();
rank.forEach(function (_, id) {
var n = g.nodes.get(id), out = function (j) { return !rank.has(j); };
var ups = unique(parentsOf(n).filter(out)), downs = unique(childrenOf(n).filter(out));
ups.concat(downs).forEach(function (j) { hidden.add(j); });
if (ups.length || downs.length) more.set(id, { up: ups, down: downs });
});
return { seeds: new Set(seeds), rank: rank, expanded: added, reach: reach, truncated: reach > kept, more: more, hidden: hidden.size,
edges: g.edges.filter(function (e) { return rank.has(e.from) && rank.has(e.to); }) };
}
function unique(list) { return list.filter(function (x, i) { return list.indexOf(x) === i; }); }
function erRows(n, edges) {
var keyCols = [], fkCols = [], rows = [];
n.keys.forEach(function (k) { k.columns.forEach(function (c) { if (keyCols.indexOf(c) < 0) keyCols.push(c); }); });
edges.forEach(function (e) {
if (e.from === n.id) e.fromColumns.forEach(function (c) { if (fkCols.indexOf(c) < 0) fkCols.push(c); });
if (e.to === n.id) e.toColumns.forEach(function (c) { if (keyCols.indexOf(c) < 0 && fkCols.indexOf(c) < 0) keyCols.push(c); });
});
keyCols.forEach(function (c) { rows.push({ name: c, mark: "key" }); });
fkCols.forEach(function (c) { if (keyCols.indexOf(c) < 0) rows.push({ name: c, mark: "fk" }); });
var rest = n.columns.filter(function (c) { return keyCols.indexOf(c) < 0 && fkCols.indexOf(c) < 0; });
var room = Math.max(0, ER.COLUMNS - rows.length);
rest.slice(0, room).forEach(function (c) { rows.push({ name: c, mark: "" }); });
return { rows: rows, hidden: rest.length - Math.min(room, rest.length) };
}
/* Boxes for a window, one row per rank, each placed under the tables it relates
to in the rows above. */
function erLayout(g, win) {
var levels = new Map();
win.rank.forEach(function (d, id) { addTo(levels, d, id); });
var order = Array.from(levels.keys()).sort(function (a, b) { return a - b; }), boxes = new Map(), placedX = new Map();
var y = 0, left = Infinity, right = -Infinity;
order.forEach(function (d) {
var ids = levels.get(d);
var bary = new Map(ids.map(function (id) {
var n = g.nodes.get(id), near = parentsOf(n).concat(childrenOf(n)).filter(function (k) { return placedX.has(k); }).map(function (k) { return placedX.get(k); });
return [id, near.length ? near.reduce(function (a, b) { return a + b; }, 0) / near.length : 0];
}));
ids.sort(function (a, b) { return bary.get(a) - bary.get(b) || compare(g.nodes.get(a).label, g.nodes.get(b).label) || compare(a, b); });
for (var start = 0; start < ids.length; start += ER.WRAP) {
var line = ids.slice(start, start + ER.WRAP);
var rows = line.map(function (id) { return erRows(g.nodes.get(id), win.edges); });
var heights = rows.map(function (r) { return ER.HEAD + Math.max(1, r.rows.length + (r.hidden ? 1 : 0)) * ER.ROW + 8; });
var width = line.length * ER.BOX + (line.length - 1) * ER.GAP_X, x = -width / 2;
line.forEach(function (id, i) {
boxes.set(id, { x: x, y: y, h: heights[i], rows: rows[i].rows, hidden: rows[i].hidden });
placedX.set(id, x + ER.BOX / 2);
left = Math.min(left, x); right = Math.max(right, x + ER.BOX);
x += ER.BOX + ER.GAP_X;
});
y += Math.max.apply(null, heights) + (start + ER.WRAP < ids.length ? ER.GAP_ROW / 2 : ER.GAP_ROW);
}
});
return { boxes: boxes, bounds: { x: left - 80, y: -80, w: right - left + 160, h: y - ER.GAP_ROW + 160 } };
}
/* The ER page's workspace, framed as the Load orchestration graph is: s holds
the selection, depths, expansions and viewport. options.item limits it to one
item's relationships; options.tools come first in its toolbar; options.onPick
hears a table chosen in the diagram, options.describe fills the details, and
options.matches(term) lists the tables a wildcard term selects. */
function erWorkspace(body, m, s, options) {
var g = erGraph(m, options.item);
s.selection = (s.selection || []).filter(function (id) { return g.nodes.has(id); });
s.expanded = (s.expanded || []).filter(function (id) { return g.nodes.has(id); });
if (s.up === undefined) s.up = 1;
if (s.down === undefined) s.down = 1;
s.moved = s.moved || {};
s.patterns = s.patterns || [];
var matched = new Map();
function matches(q) {
if (!matched.has(q)) matched.set(q, (options.matches ? options.matches(q) : []).filter(function (id) { return g.nodes.has(id); }));
return matched.get(q);
}
/* The selected tables and every match of each wildcard term. */
function seeds() {
var out = s.selection.slice(), seen = new Set(out);
s.patterns.forEach(function (q) { matches(q).forEach(function (id) { if (!seen.has(id)) { seen.add(id); out.push(id); } }); });
return out;
}
var f = workspaceFrame(s, function () {}), drawing = el("div", { "class": "wd-er-drawing" }), zoom = null, notice = null;
function focus() { return s.selection[s.selection.length - 1] || null; }
function setPatterns(list) { s.patterns = list; s.expanded = []; s.moved = {}; s.view = null; notice = null; draw(); saveState(); }
/* A plain choice replaces the selection; Shift, Ctrl or ⌘ adds or removes. */
function select(id, adding) {
if (!id) { s.selection = []; s.patterns = []; }
else if (adding) {
var at = s.selection.indexOf(id);
if (at >= 0) s.selection.splice(at, 1); else s.selection.push(id);
} else s.selection = [id];
s.expanded = []; s.moved = {}; s.view = null; notice = null;
draw();
saveState();
}
function expand(id, side) {
var hidden = win().more.get(id)[side].slice().sort(function (a, b) { return compare(g.nodes.get(a).label, g.nodes.get(b).label) || compare(a, b); });
var before = zoom && zoom.screenOf(id);
s.expanded = s.expanded.concat(hidden.slice(0, BUDGET.REVEAL).filter(function (k) { return s.expanded.indexOf(k) < 0; }));
draw(id, before);
saveState();
}
function win() { return erWindow(g, seeds(), s.up, s.down, s.expanded); }
function status(w) {
f.line.textContent = "";
var parts = [];
if (w) {
parts.push(fmt(w.rank.size) + " of " + fmt(g.nodes.size) + " tables shown" + (w.seeds.size > 1 ? " · " + w.seeds.size + " selected" : ""));
if (!w.seeds.size && w.truncated) parts.push("the most related; search or select a table to follow its relationships");
if (w.seeds.size && !w.edges.length && !w.hidden) parts.push(w.seeds.size > 1 ? "none has a declared relationship" : "it has no declared relationship");
if (w.expanded.size) parts.push(fmt(w.expanded.size) + " expanded");
if (w.hidden) parts.push(fmt(w.hidden) + " more beside them; select a ↑ or ↓ marker to expand");
if (w.seeds.size && w.truncated) parts.push(el("b", { "class": "wd-warn-text", text: "cut to the " + ER.NODES + " nearest of " + fmt(w.reach) + "; lower a depth" }));
}
if (notice) parts.push(el("b", { "class": "wd-warn-text", text: notice }));
parts.forEach(function (p, i) { if (i) f.line.appendChild(document.createTextNode(" · ")); f.line.appendChild(typeof p === "string" ? document.createTextNode(p) : p); });
}
function renderChips() {
selectionChips(f.chips, s.selection, focus(), function (id) { var n = g.nodes.get(id); return { kind: n.owner ? n.owner.kind : "Table", label: n.label, title: n.item + " · " + n.label }; },
function (id) { if (options.onPick) options.onPick(id); if (zoom) zoom.fitBoxes([id]); }, function (id, adding) { select(id, adding); if (id && options.onPick && s.selection.indexOf(id) >= 0) options.onPick(id); },
{ list: s.patterns, count: function (q) { return matches(q).length; }, remove: function (q) { setPatterns(s.patterns.filter(function (p) { return p !== q; })); } });
}
/* An edge's path and its two cardinality marks, from where its boxes are now. */
function route(e, boxes) {
var a = boxes.get(e.from), b = boxes.get(e.to), ax, ay, bx, by;
if (e.from === e.to) {
ax = a.x + ER.BOX; ay = a.y + ER.HEAD;
return { d: "M" + ax + " " + ay + "C" + (ax + 44) + " " + (ay - 10) + " " + (ax + 44) + " " + (ay + 36) + " " + ax + " " + (ay + 26) };
}
ax = a.x + ER.BOX / 2; bx = b.x + ER.BOX / 2;
if (Math.abs(a.y - b.y) < 1) {
ay = a.y; by = b.y;
var lift = Math.min(90, 30 + Math.abs(bx - ax) / 6);
return { d: "M" + ax + " " + ay + "C" + ax + " " + (ay - lift) + " " + bx + " " + (by - lift) + " " + bx + " " + by,
from: [ax + 6, ay - 8], to: [bx + 6, by - 8] };
}
var down = a.y < b.y;
ay = down ? a.y + a.h : a.y; by = down ? b.y : b.y + b.h;
var c = Math.max(30, Math.abs(by - ay) / 2) * (down ? 1 : -1);
return { d: "M" + ax + " " + ay + "C" + ax + " " + (ay + c) + " " + bx + " " + (by - c) + " " + bx + " " + by,
from: [ax + 6, ay + (down ? 12 : -5)], to: [bx + 6, by + (down ? -5 : 12)] };
}
/* Draw the window; given pin, keep that table where it was on screen. */
function draw(pin, screen) {
drawing.textContent = "";
var w = win();
status(w);
renderChips();
if (!w) { drawing.appendChild(empty("Search for a table, or select one, to draw its relationships.")); zoom = null; return; }
var lay = erLayout(g, w), boxes = lay.boxes, current = focus();
Object.keys(s.moved).forEach(function (id) { var b = boxes.get(id); if (b) { b.x = s.moved[id].x; b.y = s.moved[id].y; } });
var svg = sv("svg", { "class": "wd-er-svg", role: "img", "aria-label": "Relationship diagram" }), stage = sv("g"), lines = sv("g");
svg.appendChild(stage);
stage.appendChild(lines);
var drawn = w.edges.map(function (e) {
var r = route(e, boxes), lit = w.seeds.has(e.from) || w.seeds.has(e.to), d = { e: e };
d.path = lines.appendChild(sv("path", { "class": "wd-er-edge" + (e.active ? "" : " wd-er-inactive") + (lit ? " wd-er-focus" : ""), d: r.d },
[sv("title", {}, [(e.label ? e.label + ": " : "") + g.nodes.get(e.from).label + " (" + e.fromColumns.join(", ") + ") → " + g.nodes.get(e.to).label + " (" + e.toColumns.join(", ") + ")" + (e.active ? "" : " · inactive")])]));
if (r.from) {
d.many = lines.appendChild(sv("text", { "class": "wd-er-card", x: r.from[0], y: r.from[1] }, [e.many === false ? "1" : "*"]));
d.one = lines.appendChild(sv("text", { "class": "wd-er-card", x: r.to[0], y: r.to[1] }, [e.one === false ? "*" : "1"]));
}
return d;
});
function reroute(id) {
drawn.forEach(function (d) {
if (d.e.from !== id && d.e.to !== id) return;
var r = route(d.e, boxes);
d.path.setAttribute("d", r.d);
if (d.many) { d.many.setAttribute("x", r.from[0]); d.many.setAttribute("y", r.from[1]); d.one.setAttribute("x", r.to[0]); d.one.setAttribute("y", r.to[1]); }
});
}
boxes.forEach(function (box, id) {
var n = g.nodes.get(id), seed = w.seeds.has(id);
var group = sv("g", { "class": "wd-er-box" + (seed ? " wd-er-box-focus" : "") + (id === current ? " wd-er-box-current" : ""), transform: "translate(" + box.x + " " + box.y + ")", tabindex: "0", role: "button", "aria-label": n.label });
group.appendChild(sv("rect", { width: ER.BOX, height: box.h, rx: 9 }));
group.appendChild(sv("rect", { "class": "wd-er-head", width: ER.BOX, height: ER.HEAD - 6, rx: 9 }));
group.appendChild(sv("text", { "class": "wd-er-title", x: 12, y: 17 }, [clipText(n.label, 28)]));
group.appendChild(sv("text", { "class": "wd-er-item", x: 12, y: 29 }, [clipText(itemName(n.item), 34)]));
box.rows.forEach(function (r, i) {
group.appendChild(sv("text", { "class": "wd-er-col" + (r.mark ? " wd-er-" + r.mark : ""), x: 12, y: ER.HEAD + i * ER.ROW + 13 },
[(r.mark === "key" ? "⚿ " : r.mark === "fk" ? "↗ " : "   ") + clipText(r.name, 30)]));
});
if (box.hidden) group.appendChild(sv("text", { "class": "wd-er-col wd-er-hidden", x: 12, y: ER.HEAD + box.rows.length * ER.ROW + 13 }, [box.hidden + " more described columns"]));
var more = w.more.get(id);
if (more && more.up.length) group.appendChild(marker(box, id, "up", more.up.length));
if (more && more.down.length) group.appendChild(marker(box, id, "down", more.down.length));
draggable(group, box, id, reroute);
group.addEventListener("keydown", function (ev) { if (ev.key === "Enter") pickBox(id, ev.shiftKey || ev.metaKey || ev.ctrlKey); });
stage.appendChild(group);
});
drawing.appendChild(svg);
zoom = panZoom(svg, stage, s, lay.bounds, boxes);
if (pin && screen) zoom.pin(pin, screen);
}
/* A mouse or pen drag moves a box and the edges meeting it; a press that
does not move selects it. */
function draggable(group, box, id, reroute) {
var drag = null;
group.addEventListener("pointerdown", function (ev) {
if (ev.button !== 0 || (ev.target.closest && ev.target.closest(".wd-er-more"))) return;
drag = { x: ev.clientX, y: ev.clientY, from: { x: box.x, y: box.y }, moved: false, touch: ev.pointerType === "touch" };
if (!drag.touch) group.setPointerCapture(ev.pointerId);
});
group.addEventListener("pointermove", function (ev) {
if (!drag || drag.touch) return;
var dx = ev.clientX - drag.x, dy = ev.clientY - drag.y, k = s.view ? s.view.k : 1;
if (!drag.moved && Math.hypot(dx, dy) < 4) return;
drag.moved = true;
box.x = drag.from.x + dx / k; box.y = drag.from.y + dy / k;
group.setAttribute("transform", "translate(" + box.x + " " + box.y + ")");
group.classList.add("wd-dragging");
reroute(id);
});
function end(ev) {
if (!drag) return;
var was = drag;
drag = null;
group.classList.remove("wd-dragging");
if (ev.type !== "pointerup") return;
if (was.moved) { s.moved[id] = { x: box.x, y: box.y }; saveState(); }
else pickBox(id, ev.shiftKey || ev.metaKey || ev.ctrlKey);
}
group.addEventListener("pointerup", end);
group.addEventListener("pointercancel", end);
}
function marker(box, id, side, count) {
var text = (side === "up" ? "↑ " : "↓ ") + count, w = 12 + text.length * 6.4;
var badge = sv("g", { "class": "wd-er-more", tabindex: "0", role: "button", transform: "translate(" + (ER.BOX - w - 10) + " " + (side === "up" ? -9 : box.h - 8) + ")" },
[sv("rect", { width: w, height: 17, rx: 8.5 }), sv("text", { x: w / 2, y: 12 }, [text]),
sv("title", {}, [count + (side === "up" ? (count === 1 ? " parent table" : " parent tables") : (count === 1 ? " child table" : " child tables")) + " not shown. Select to show " + (count > BUDGET.REVEAL ? "the first " + BUDGET.REVEAL : count === 1 ? "it" : "them") + "."])]);
badge.addEventListener("pointerdown", function (ev) { ev.stopPropagation(); });
badge.addEventListener("click", function (ev) { ev.stopPropagation(); expand(id, side); });
badge.addEventListener("keydown", function (ev) { ev.stopPropagation(); if (ev.key === "Enter") expand(id, side); });
return badge;
}
function pickBox(id, adding) {
select(id, adding);
if (options.onPick && s.selection.indexOf(id) >= 0) options.onPick(id);
}
f.mount(body, (options.tools || []).concat([
segmented("Parents", DEPTHS, s.up, function (d) { s.up = d; s.expanded = []; s.moved = {}; s.view = null; draw(); saveState(); }, depthLabel),
segmented("Children", DEPTHS, s.down, function (d) { s.down = d; s.expanded = []; s.moved = {}; s.view = null; draw(); saveState(); }, depthLabel),
el("span", { "class": "wd-grow" }),
el("div", { "class": "wd-zoom" }, [
el("button", { "class": "wd-icon", type: "button", title: "Zoom out", "aria-label": "Zoom out", onclick: function () { if (zoom) zoom.zoomBy(0.8); } }, ["−"]),
el("button", { "class": "wd-icon", type: "button", title: "Zoom in", "aria-label": "Zoom in", onclick: function () { if (zoom) zoom.zoomBy(1.25); } }, ["+"]),
el("button", { "class": "wd-text-btn", type: "button", title: "Fit what is shown", onclick: function () { if (zoom) zoom.fit(); } }, ["Fit"])
])
]));
f.host.classList.add("wd-er");
f.host.appendChild(drawing);
f.legend.appendChild(el("div", { "class": "wd-legend" }, [
el("span", { "class": "wd-key", text: "⚿ key column" }), el("span", { "class": "wd-key", text: "↗ foreign key column" }),
el("span", { "class": "wd-key", text: "* many · 1 one" }), el("span", { "class": "wd-key" }, [el("i", { "class": "wd-key-line wd-up" }), "Relationship of a selected table"]),
el("span", { "class": "wd-key" }, [el("i", { "class": "wd-key-more", text: "↑ 3" }), "parents not shown"]),
el("span", { "class": "wd-key" }, [el("i", { "class": "wd-key-more", text: "↓ 3" }), "children not shown: select to expand"])
]));
if (options.describe) options.describe(f.side);
if (!g.nodes.size) {
drawing.appendChild(empty("No declared table is recorded" + (options.item && options.item !== "all" ? " for " + itemName(options.item) : "") + "."));
return { has: function () { return false; }, select: function () {}, addPattern: function () {}, say: function () {}, side: f.side };
}
draw();
return {
has: function (id) { return g.nodes.has(id); },
select: function (id, adding) { if (g.nodes.has(id)) select(id, adding); },
/* A wildcard term joins the selection, whatever else is selected. */
addPattern: function (q) { if (s.patterns.indexOf(q) < 0) setPatterns(s.patterns.concat([q])); },
/* A note on the status line until the next drawing. */
say: function (text) { notice = text; status(win()); },
side: f.side
};
}
function clipText(text, n) { text = String(text || ""); return text.length > n ? text.slice(0, n - 1) + "…" : text; }
function sv(tag, attrs, children) {
var e = document.createElementNS("http://www.w3.org/2000/svg", tag);
setAttrs(e, attrs);
(children || []).forEach(function (c) { if (c) e.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
return e;
}
/* Pan and zoom for an SVG stage, with the same gestures as the graph. */
function panZoom(svg, stage, s, bounds, boxes) {
function box() { return svg.getBoundingClientRect(); }
function apply() { stage.setAttribute("transform", "translate(" + s.view.x + " " + s.view.y + ") scale(" + s.view.k + ")"); }
function fitRect(r) {
var b = box(), k = Math.min(1.1, Math.max(0.15, Math.min(b.width / r.w, b.height / r.h)));
s.view = { k: k, x: b.width / 2 - (r.x + r.w / 2) * k, y: b.height / 2 - (r.y + r.h / 2) * k };
apply();
}
function fit() { fitRect(bounds); }
if (s.view) apply(); else (root.requestAnimationFrame || setTimeout)(fit);
var drag = null;
svg.addEventListener("pointerdown", function (e) {
if (e.target.closest && (e.target.closest(".wd-er-box") || e.target.closest(".wd-er-more"))) return;
drag = { x: e.clientX, y: e.clientY, v: s.view, touch: e.pointerType === "touch" };
});
svg.addEventListener("pointermove", function (e) {
if (!drag || !s.view) return;
s.view = { k: drag.v.k, x: drag.v.x + e.clientX - drag.x, y: drag.v.y + (drag.touch ? 0 : e.clientY - drag.y) };
apply();
});
["pointerup", "pointercancel", "pointerleave"].forEach(function (t) { svg.addEventListener(t, function () { drag = null; }); });
function zoomAt(f, px, py) {
var k = Math.min(2.5, Math.max(0.1, s.view.k * f));
f = k / s.view.k;
s.view = { k: k, x: px - (px - s.view.x) * f, y: py - (py - s.view.y) * f };
apply();
}
svg.addEventListener("wheel", function (e) {
if (!(e.ctrlKey || e.metaKey) && pageScrolls()) return;
e.preventDefault();
var b = box();
zoomAt(Math.exp(-e.deltaY * 0.0025), e.clientX - b.left, e.clientY - b.top);
}, { passive: false });
return {
fit: fit,
zoomBy: function (f) { if (!s.view) return; var b = box(); zoomAt(f, b.width / 2, b.height / 2); },
fitBoxes: function (ids) {
var x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
ids.forEach(function (id) { var b = boxes.get(id); if (b) { x0 = Math.min(x0, b.x); y0 = Math.min(y0, b.y); x1 = Math.max(x1, b.x + ER.BOX); y1 = Math.max(y1, b.y + b.h); } });
if (x0 < Infinity) fitRect({ x: x0 - 200, y: y0 - 160, w: x1 - x0 + 400, h: y1 - y0 + 320 });
},
screenOf: function (id) { var b = boxes.get(id); return b && s.view ? { x: b.x * s.view.k + s.view.x, y: b.y * s.view.k + s.view.y } : null; },
pin: function (id, screen) { var b = boxes.get(id); if (!b || !s.view) return; s.view = { k: s.view.k, x: screen.x - b.x * s.view.k, y: screen.y - b.y * s.view.k }; apply(); }
};
}
var GANTT = { LABEL: 280, ROW: 20, AXIS: 28 };
function logRows(m) {
if (m.logRows) return m.logRows;
var byTarget = new Map(), flows = new Map((m.tables.logflows || []).map(function (r) { return [r.index, r.workflow]; }));
m.items.forEach(function (it) { if (it.target) byTarget.set(it.type + "|" + it.target, it.label); });
m.logRows = (m.tables.log || []).filter(function (r) {
var item = byTarget.get(r.targettype + "|" + r.target);
return !(item && isInternal(m, item, r.schema)) && !(r.object && INTERNAL_SCHEMA.test(r.schema || ""));
}).map(function (r) {
var item = byTarget.get(r.targettype + "|" + r.target) || null;
var node = item && r.object ? m.byIdentity.get(identityKey(item, r.schema, r.object)) || null : null;
var started = num(r.started), completed = num(r.completed);
return { id: r.id, workflow: flows.get(r.flow) || null, task: r.task, target: r.target, schema: r.schema, object: r.object, result: r.result,
started: started !== null ? started : completed, completed: completed !== null ? completed : started, duration: num(r.duration),
node: node, message: r.message, envelope: !r.object,
label: node ? node.label : r.object ? qualified({ item: item, schema: r.schema, object: r.object }) : (r.message || r.task || "") };
});
return m.logRows;
}
/* Elapsed span, summed task time and peak concurrency of processed records. */
function ganttSummary(rows) {
var t0 = Infinity, t1 = -Infinity, work = 0, events = [];
rows.forEach(function (r) {
if (r.started === null) return;
t0 = Math.min(t0, r.started); t1 = Math.max(t1, r.completed);
work += Math.max(0, r.completed - r.started);
if (!r.envelope) { events.push([r.started, 1]); events.push([r.completed, -1]); }
});
events.sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; });
var running = 0, peak = 0;
events.forEach(function (e) { running += e[1]; peak = Math.max(peak, running); });
return { t0: t0, t1: Math.max(t1, t0 + 1000), span: t1 > t0 ? t1 - t0 : 0, work: work, peak: peak };
}
function ganttPage(body, m) {
var s = pageState("gantt"), all = logRows(m), flows = m.workflows || [];
var included = new Map((m.tables.logflows || []).map(function (r) { return [r.workflow, { records: num(r.records), included: num(r.included) }]; }));
if (!flows.length) { body.appendChild(empty("No workflow has processed a record in the last 7 days. Run weaver load to see its timeline.")); return; }
if (!s.workflow || !flows.some(function (w) { return w.id === s.workflow; }) || s.follow !== false) s.workflow = flows[0].id;
s.scope = s.scope || "objects";
var select = el("select", { "class": "wd-select", "aria-label": "Workflow", onchange: function () {
s.workflow = this.value; s.follow = this.selectedIndex === 0; s.zoom = null; render(); saveState();
} }, flows.map(function (w, i) {
return el("option", { value: w.id, selected: w.id === s.workflow ? "selected" : null,
text: (i === 0 ? "Latest · " : "") + stamp(w.started).slice(0, 16) + " · " + duration((w.completed || 0) - (w.started || 0)) + " · " + fmt(w.records) + " records" + (w.failed ? " · " + w.failed + " failed" : "") + " · " + w.id.slice(0, 8) });
}));
var host = el("div");
body.appendChild(el("div", { "class": "wd-toolbar" }, [select,
segmented("Show", ["objects", "all"], s.scope, function (v) { s.scope = v; render(); saveState(); }, function (v) { return v === "objects" ? "Objects" : "All records"; }),
el("span", { "class": "wd-grow" }),
el("span", { "class": "wd-muted", text: "Ctrl or ⌘ and scroll to zoom time; drag to pan; double-click to reset" })]));
body.appendChild(host);
function render() {
host.textContent = "";
var flow = flows.filter(function (w) { return w.id === s.workflow; })[0], have = included.get(s.workflow);
var rows = all.filter(function (r) { return r.workflow === s.workflow; });
if (!have || !have.included) {
host.appendChild(el("div", { "class": "wd-banner wd-banner-warn", text: "This page carries the records of the 12 latest workflows, up to 20,000 records. This workflow's " + fmt(flow.records) + " records are not among them." }));
return;
}
if (have.included < have.records) {
host.appendChild(el("div", { "class": "wd-banner wd-banner-warn", text: "Showing the first " + fmt(have.included) + " of this workflow's " + fmt(have.records) + " records, by start time. The timeline is incomplete." }));
}
var sum = ganttSummary(rows), failed = rows.filter(function (r) { return tone(r.result) === "bad"; }).length;
host.appendChild(el("div", { "class": "wd-tiles" }, [
tile("Elapsed", duration(sum.span), stamp(sum.t0) + " to " + stamp(sum.t1).slice(11), "none"),
tile("Task time", duration(sum.work), "summed over records; overlaps count twice", "none"),
tile("Peak concurrency", sum.peak, "object records running at once", "none"),
tile("Records", rows.length, flow.tasks.join(", "), "none"),
tile("Failed", failed, "Failed, Error or Blocked", failed ? "bad" : "ok")
]));
var shown = rows.filter(function (r) { return s.scope === "all" || !r.envelope; }).filter(function (r) { return r.started !== null; });
shown.sort(function (a, b) { return a.started - b.started || compare(a.label, b.label) || compare(a.id, b.id); });
if (!shown.length) { host.appendChild(empty("No object record has been processed for this workflow.")); return; }
host.appendChild(ganttChart(shown, sum, s, m));
}
render();
}
function ganttChart(rows, sum, s, m) {
var wrap = el("div", { "class": "wd-gantt", style: "height:" + (GANTT.AXIS + rows.length * GANTT.ROW + 8) + "px" });
var canvas = el("canvas", { "class": "wd-gantt-canvas" }), tip = el("div", { "class": "wd-tip", hidden: "hidden" });
wrap.appendChild(canvas); wrap.appendChild(tip);
s.zoom = s.zoom || { a: 0, b: 1 };
var P = null, width = 0, height = 0, ratio = 1, top = 0;
function measure() {
var box = wrap.getBoundingClientRect(), clip = clipRect(wrap);
width = Math.max(320, box.width);
top = Math.max(0, clip.top - box.top); height = Math.min(box.height, clip.bottom - box.top) - top;
ratio = canvasRatio(width, height);
canvas.style.top = top + "px"; canvas.style.width = width + "px"; canvas.style.height = Math.max(0, height) + "px";
canvas.width = Math.round(width * ratio); canvas.height = Math.round(Math.max(1, height) * ratio);
}
function time(t) { var span = sum.t1 - sum.t0, a = sum.t0 + span * s.zoom.a, b = sum.t0 + span * s.zoom.b; return GANTT.LABEL + (t - a) / (b - a) * (width - GANTT.LABEL - 16); }
function paint() {
measure();
if (height <= 0) return;
P = P || paletteOf(wrap);
var ctx = canvas.getContext("2d"), span = sum.t1 - sum.t0;
ctx.setTransform(ratio, 0, 0, ratio, 0, -top * ratio);
ctx.clearRect(0, top, width, height);
var first = Math.max(0, Math.floor((top - GANTT.AXIS) / GANTT.ROW)), last = Math.min(rows.length, Math.ceil((top + height) / GANTT.ROW));
ctx.font = "11px " + P.sans; ctx.textBaseline = "middle";
for (var i = first; i < last; i++) {
var r = rows[i], y = GANTT.AXIS + i * GANTT.ROW;
if (i % 2) { ctx.fillStyle = P["paper-deep"]; ctx.globalAlpha = 0.45; ctx.fillRect(0, y, width, GANTT.ROW); ctx.globalAlpha = 1; }
ctx.fillStyle = r.envelope ? P.muted : P.ink;
ctx.fillText(clip(ctx, r.label + (r.envelope ? " · " + r.task : ""), GANTT.LABEL - 18, "11px " + P.sans), 8, y + GANTT.ROW / 2);
var x1 = Math.max(GANTT.LABEL, time(r.started)), x2 = Math.min(width - 8, time(r.completed));
if (x2 >= GANTT.LABEL && x1 <= width - 8) {
ctx.fillStyle = toneColour(tone(r.result), P);
ctx.globalAlpha = r.envelope ? 0.35 : 0.9;
ctx.beginPath(); roundRect(ctx, x1, y + 4, Math.max(2.5, x2 - x1), GANTT.ROW - 8, 3); ctx.fill(); ctx.globalAlpha = 1;
}
}
var axisY = Math.max(top, 0);
ctx.fillStyle = P.surface; ctx.fillRect(0, axisY, width, GANTT.AXIS);
ctx.strokeStyle = P.line; ctx.beginPath(); ctx.moveTo(0, axisY + GANTT.AXIS - 0.5); ctx.lineTo(width, axisY + GANTT.AXIS - 0.5); ctx.stroke();
var a = sum.t0 + span * s.zoom.a, b = sum.t0 + span * s.zoom.b, plot = width - GANTT.LABEL - 16;
ctx.fillStyle = P.ink; ctx.font = "600 10.5px " + P.mono;
var startText = clockLabel(a, null), startEnd = GANTT.LABEL + 4 + ctx.measureText(startText).width + 18;
ctx.fillText(startText, GANTT.LABEL + 4, axisY + 14);
ctx.fillStyle = P.muted; ctx.font = "10.5px " + P.mono;
var previous = a;
clockTicks(a, b, plot).forEach(function (t) {
var gx = time(t);
ctx.globalAlpha = 0.5; ctx.beginPath(); ctx.moveTo(gx, axisY + GANTT.AXIS); ctx.lineTo(gx, top + height); ctx.stroke(); ctx.globalAlpha = 1;
if (gx < startEnd || gx > width - 60) return;
ctx.fillText(clockLabel(t, previous), gx + 3, axisY + 14);
previous = t;
});
ctx.fillStyle = P.muted; ctx.font = "600 10px " + P.mono; ctx.fillText("RECORD · UTC", 8, axisY + 14);
}
function schedule() { (root.requestAnimationFrame || setTimeout)(paint); }
onAnyScroll(wrap, schedule);
if (root.ResizeObserver) new root.ResizeObserver(schedule).observe(wrap);
schedule();
wrap.addEventListener("wheel", function (e) {
if (!(e.ctrlKey || e.metaKey)) return;
e.preventDefault();
var box = wrap.getBoundingClientRect(), f = Math.min(1, Math.max(0, (e.clientX - box.left - GANTT.LABEL) / (width - GANTT.LABEL - 16)));
var a = s.zoom.a, b = s.zoom.b, at = a + (b - a) * f, w = Math.min(1, Math.max(0.0005, (b - a) * Math.exp(e.deltaY * 0.002)));
s.zoom.a = Math.max(0, Math.min(1 - w, at - w * f)); s.zoom.b = s.zoom.a + w;
schedule();
}, { passive: false });
var drag = null;
wrap.addEventListener("pointerdown", function (e) { if (e.pointerType !== "touch") drag = { x: e.clientX, a: s.zoom.a, b: s.zoom.b }; });
wrap.addEventListener("pointermove", function (e) {
var box = wrap.getBoundingClientRect();
if (drag) {
var w = drag.b - drag.a, d = -(e.clientX - drag.x) / (width - GANTT.LABEL - 16) * w;
s.zoom.a = Math.max(0, Math.min(1 - w, drag.a + d)); s.zoom.b = s.zoom.a + w;
schedule(); return;
}
var i = Math.floor((e.clientY - box.top - GANTT.AXIS) / GANTT.ROW), r = rows[i];
if (!r || e.clientY - box.top < GANTT.AXIS) { tip.hidden = true; return; }
tip.textContent = "";
tip.appendChild(el("b", { text: r.label }));
tip.appendChild(el("div", {}, [chip(r.result), " " + r.task + " · " + duration(r.completed - r.started)]));
tip.appendChild(el("div", { "class": "wd-muted", text: stamp(r.started) + " → " + stamp(r.completed).slice(11) }));
if (r.message && r.object) tip.appendChild(el("div", { "class": "wd-tip-message", text: r.message }));
tip.hidden = false;
tip.style.left = Math.min(box.width - 270, e.clientX - box.left + 14) + "px";
tip.style.top = (e.clientY - box.top + 14) + "px";
});
["pointerup", "pointercancel"].forEach(function (t) { wrap.addEventListener(t, function () { drag = null; }); });
wrap.addEventListener("pointerleave", function () { drag = null; tip.hidden = true; });
wrap.addEventListener("dblclick", function () { s.zoom = { a: 0, b: 1 }; schedule(); });
return wrap;
}
var CLOCK_STEPS = [1, 2, 5, 10, 15, 30, 60, 120, 300, 600, 900, 1800, 3600, 7200, 10800, 21600, 43200, 86400]
.map(function (seconds) { return seconds * 1000; });
/* Round instants between a and b, about one per 110 px. */
function clockTicks(a, b, width) {
var room = Math.max(2, Math.floor(width / 110)), step = null;
for (var i = 0; i < CLOCK_STEPS.length && step === null; i++) if ((b - a) / CLOCK_STEPS[i] <= room) step = CLOCK_STEPS[i];
if (step === null) step = 86400000 * Math.ceil((b - a) / 86400000 / room);
var out = [];
for (var t = Math.ceil(a / step) * step; t <= b; t += step) out.push(t);
return out;
}
/* hh:mm:ss, preceded by the date when it differs from the previous label's. */
function clockLabel(t, previous) {
var iso = new Date(t).toISOString(), day = iso.slice(0, 10), clock = iso.slice(11, 19);
return previous === null || new Date(previous).toISOString().slice(0, 10) !== day ? day + " " + clock : clock;
}
function paletteOf(node) {
var cs = root.getComputedStyle(node), P = {};
["ink", "muted", "faint", "line", "line-strong", "surface", "paper", "paper-deep", "blue", "blue-dark", "green", "amber", "red", "violet", "sans", "mono"]
.forEach(function (name) { P[name] = cs.getPropertyValue("--" + name).trim(); });
return P;
}
function perfRows(m, name) {
return (m.tables[name] || []).filter(function (r) { return !isInternal(m, r.item, r.schema); }).map(function (r) {
var node = m.byIdentity.get(identityKey(r.item, r.schema, r.object)) || null;
return { item: r.item, schema: r.schema, object: r.object, node: node, label: node ? node.label : r.schema + "." + r.object,
loads: num(r.loads) || 0, duration: num(r.duration), longest: num(r.longest), read: num(r.read), inserted: num(r.inserted),
updated: num(r.updated), deleted: num(r.deleted), rejected: num(r.rejected), reloads: num(r.reloads) || 0, skips: num(r.skips) || 0,
timedRead: num(r.timedread), timedDuration: num(r.timedduration), last: num(r.last) };
});
}
function changed(r) {
if (r.inserted === null && r.updated === null && r.deleted === null) return null;
return (r.inserted || 0) + (r.updated || 0) + (r.deleted || 0);
}
function sumOf(rows, f) {
var total = null;
rows.forEach(function (r) { var v = f(r); if (v !== null && v !== undefined) total = (total || 0) + v; });
return total;
}
function throughput(read, ms) { return read === null || !ms ? null : read / (ms / 1000); }
function performancePage(body, m) {
var s = pageState("performance");
if (["day", "week", "month"].indexOf(s.window) < 0) s.window = "month";
s.item = s.item || "all";
var host = el("div");
var items = Array.from(new Set((m.tables.perftrend || []).map(function (r) { return r.item; }))).filter(function (it) { return !isInternal(m, it); }).sort(compare);
body.appendChild(el("div", { "class": "wd-toolbar" }, [
segmented("Window", ["day", "week", "month"], s.window, function (v) { s.window = v; render(); saveState(); }, function (v) { return { day: "Last 24 hours", week: "Last 7 days", month: "Last 30 days" }[v]; }),
el("select", { "class": "wd-select", "aria-label": "Item", onchange: function () { s.item = this.value; render(); saveState(); } },
[el("option", { value: "all", text: "Every item" })].concat(items.map(function (it) { return el("option", { value: it, selected: it === s.item ? "selected" : null, text: it }); })))
]));
body.appendChild(host);
function render() {
host.textContent = "";
var rows = perfRows(m, "perf" + s.window).filter(function (r) { return s.item === "all" || r.item === s.item; });
var loads = sumOf(rows, function (r) { return r.loads; }) || 0, time = sumOf(rows, function (r) { return r.duration; });
var read = sumOf(rows, function (r) { return r.read; }), change = sumOf(rows, changed), rejected = sumOf(rows, function (r) { return r.rejected; });
var tp = throughput(sumOf(rows, function (r) { return r.timedRead; }), sumOf(rows, function (r) { return r.timedDuration; }));
host.appendChild(el("div", { "class": "wd-tiles" }, [
tile("Loads", loads, sumOf(rows, function (r) { return r.reloads; }) + " reloads · " + sumOf(rows, function (r) { return r.skips; }) + " static skips", "none"),
tile("Load time", duration(time), "summed over loads, not elapsed", "none"),
tile("Rows read", read === null ? "—" : fmt(read), "source rows processed", "none"),
tile("Rows changed", change === null ? "—" : fmt(change), "inserted + updated + deleted", "none"),
tile("Rows rejected", rejected === null ? "—" : fmt(rejected), rejected ? "see the objects below" : "", rejected ? "warn" : "none"),
tile("Throughput", tp === null ? "—" : fmt(Math.round(tp)) + "/s", "rows read per second of load time", "none")
]));
host.appendChild(section("Daily trend, last 30 days", [trendChart(m, s.item)]));
var columns = [
{ key: "object", title: "Object", value: function (r) { return r.label; }, render: function (r) { return r.node ? el("span", {}, [kindMark(r.node.kind), r.label]) : r.label; } },
{ key: "item", title: "Item", value: function (r) { return itemName(r.item); } },
{ key: "loads", title: "Loads", value: function (r) { return r.loads; }, numeric: true },
{ key: "duration", title: "Time", value: function (r) { return r.duration; }, render: function (r) { return duration(r.duration); }, numeric: true },
{ key: "longest", title: "Longest", value: function (r) { return r.longest; }, render: function (r) { return duration(r.longest); }, numeric: true },
{ key: "read", title: "Read", value: function (r) { return r.read; }, render: function (r) { return fmt(r.read); }, numeric: true },
{ key: "changed", title: "Changed", value: changed, render: function (r) { return fmt(changed(r)); }, numeric: true },
{ key: "rejected", title: "Rejected", value: function (r) { return r.rejected; }, render: function (r) { return fmt(r.rejected); }, numeric: true },
{ key: "throughput", title: "Rows/s", value: function (r) { return throughput(r.timedRead, r.timedDuration); }, render: function (r) { var v = throughput(r.timedRead, r.timedDuration); return v === null ? "—" : fmt(Math.round(v)); }, numeric: true },
{ key: "last", title: "Last", value: function (r) { return r.last; }, render: function (r) { return ago(r.last, m.at); }, numeric: true }
];
host.appendChild(section("Objects · " + fmt(rows.length), [dataTable(columns, rows, { limit: 200, sort: "duration", emptyText: "No load statistic was recorded in this window." })]));
var single = function (name) {
return (m.tables[name] || []).filter(function (r) { return !isInternal(m, r.item, r.schema) && (s.item === "all" || r.item === s.item); }).map(function (r) {
var node = m.byIdentity.get(identityKey(r.item, r.schema, r.object));
return { label: node ? node.label : r.schema + "." + r.object, item: r.item, completed: num(r.completed), duration: num(r.duration), read: num(r.read),
inserted: num(r.inserted), updated: num(r.updated), deleted: num(r.deleted), rejected: num(r.rejected), reload: !!r.reload, skip: !!r.skip, workflow: r.workflow };
});
};
var loadColumns = [
{ key: "label", title: "Object", value: function (r) { return r.label; } },
{ key: "completed", title: "Processed", value: function (r) { return r.completed; }, render: function (r) { return stamp(r.completed); }, numeric: true },
{ key: "duration", title: "Time", value: function (r) { return r.duration; }, render: function (r) { return duration(r.duration); }, numeric: true },
{ key: "changed", title: "Changed", value: changed, render: function (r) { return fmt(changed(r)); }, numeric: true },
{ key: "flags", title: "", value: function (r) { return (r.reload ? "reload " : "") + (r.skip ? "static skip" : ""); }, sortable: false }
];
host.appendChild(el("div", { "class": "wd-columns-2" }, [
section("Slowest loads, last 7 days", [dataTable(loadColumns, single("slowest"), { limit: 50, sort: "duration", emptyText: "No load in the last 7 days." })]),
section("Largest changes, last 7 days", [dataTable(loadColumns, single("largest"), { limit: 50, sort: "changed", emptyText: "No recorded row change in the last 7 days." })])
]));
}
render();
}
function trendChart(m, item) {
var days = new Map();
(m.tables.perftrend || []).forEach(function (r) {
if (isInternal(m, r.item) || (item !== "all" && r.item !== item)) return;
var d = num(r.day), e = days.get(d) || { day: d, loads: 0, duration: null, changed: null };
e.loads += num(r.loads) || 0;
if (num(r.duration) !== null) e.duration = (e.duration || 0) + num(r.duration);
if (num(r.changed) !== null) e.changed = (e.changed || 0) + num(r.changed);
days.set(d, e);
});
if (!days.size) return empty("No load statistic was recorded in the last 30 days.");
var list = [], newest = Math.max.apply(null, Array.from(days.keys())), W = 900, H = 170, pad = 34;
for (var i = 29; i >= 0; i--) { var d = newest - i * 86400000; list.push(days.get(d) || { day: d, loads: 0, duration: null, changed: null }); }
var maxTime = Math.max(1, Math.max.apply(null, list.map(function (e) { return e.duration || 0; })));
var bw = (W - pad * 2) / list.length;
var svg = sv("svg", { "class": "wd-trend", viewBox: "0 0 " + W + " " + H, role: "img", "aria-label": "Load time per day" });
[0, 0.5, 1].forEach(function (f) {
var y = H - 24 - f * (H - 44);
svg.appendChild(sv("line", { "class": "wd-grid", x1: pad, x2: W - pad, y1: y, y2: y }));
svg.appendChild(sv("text", { "class": "wd-axis", x: pad - 6, y: y + 3, "text-anchor": "end" }, [duration(maxTime * f).replace(" min", "m").replace(" s", "s")]));
});
list.forEach(function (e, i) {
var h = (e.duration || 0) / maxTime * (H - 44), x = pad + i * bw;
var bar = sv("rect", { "class": "wd-trend-bar", x: x + 2, y: H - 24 - h, width: Math.max(1, bw - 4), height: Math.max(e.loads ? 1 : 0, h), rx: 2 },
[sv("title", {}, [stamp(e.day).slice(0, 10) + ": " + fmt(e.loads) + " loads · " + duration(e.duration) + " · " + fmt(e.changed) + " rows changed"])]);
svg.appendChild(bar);
if (i % 5 === 4 || i === list.length - 1) svg.appendChild(sv("text", { "class": "wd-axis", x: x + bw / 2, y: H - 8, "text-anchor": "middle" }, [stamp(e.day).slice(5, 10)]));
});
return svg;
}
var PAGES = {
overview: overviewPage, health: healthPage, orchestration: orchestrationPage, gantt: ganttPage,
performance: performancePage, entities: entitiesPage, semantic: semanticPage
};
var STORE = "weaver-dashboard-state";
function saveState() {
try { root.sessionStorage.setItem(STORE, JSON.stringify(state())); } catch (e) { /* unavailable */ }
}
function restoreState() {
if (root.__WD_STATE) return;
try {
var raw = root.sessionStorage.getItem(STORE);
if (raw) root.__WD_STATE = JSON.parse(raw);
} catch (e) { /* unavailable */ }
}
function start() {
if (typeof document === "undefined") return;
var mount = document.getElementById("wd-app"), source = document.getElementById("wd-data");
if (!mount) return;
restoreState();
var parsed = parsePayload(source ? source.textContent : ""), m = buildModel(parsed.tables, parsed.problems);
if (!source) m.problems.push("The page carries no catalogue data.");
function render() {
var scroller = scrollBox(mount), scroll = scroller ? scroller.scrollTop : root.scrollY || 0;
mount.textContent = "";
mount.className = "wd wd-page-" + m.page;
var body = shell(mount, m);
try {
(PAGES[m.page] || overviewPage)(body, m);
} catch (error) {
body.appendChild(el("pre", { "class": "wd-error", text: "This page could not be drawn: " + (error && error.message) }));
}
if (scroll && scroller) scroller.scrollTop = scroll;
else if (scroll && root.scrollTo) root.scrollTo(0, scroll);
saveState();
}
root.__WD_REDRAW = render;
render();
root.addEventListener("pagehide", saveState);
}
var api = {
parsePayload: parsePayload, buildModel: buildModel, assessHealth: assessHealth, readiness: readiness,
layoutEstate: layoutEstate, WINDOW_GEOMETRY: WINDOW_GEOMETRY, subModel: subModel, focusWindow: focusWindow, searchNodes: searchNodes, nodeMatches: nodeMatches, dictionaryEntries: dictionaryEntries,
searchEntries: searchEntries, metadata: metadata, modelTables: modelTables, busMatrix: busMatrix, erGraph: erGraph,
erWindow: erWindow, erLayout: erLayout, ER: ER, ganttSummary: ganttSummary, clockTicks: clockTicks, clockLabel: clockLabel, canvasRatio: canvasRatio, logRows: logRows, perfRows: perfRows, tone: tone, BUDGET: BUDGET,
FIELD: FIELD, ROW: ROW, TABLE: TABLE, LESS: LESS
};
if (typeof module === "object" && module && module.exports) module.exports = api;
else { root.WeaverDashboard = api; start(); }
})(window);
