"use strict";
const fields = [
  ["question", "My question"], ["agents", "Treatment, medicines and products used"],
  ["timing", "Timing and sequence"], ["observations", "Observations and measurements"],
  ["confounders", "Other changes"], ["review", "Practitioner review and unresolved questions"],
  ["sources", "Published references to discuss"]
];
function makeNote() {
  return ["PRIVATE NOTES FOR MY LICENSED PRACTITIONER", "Personal observations, not causal evidence or a treatment plan.",
    "Share directly with your chosen practitioner through their secure channel. Do not post to GitHub.", "",
    ...fields.map(([id, label]) => label + "\n" + (document.getElementById(id).value.trim() || "Not recorded") + "\n")].join("\n");
}
document.getElementById("preview-note").addEventListener("click", () => {
  document.getElementById("preview").textContent = makeNote();
  document.getElementById("preview-section").hidden = false;
  document.getElementById("status").textContent = "Preview created here. Nothing submitted.";
});
document.getElementById("download-note").addEventListener("click", () => {
  const url = URL.createObjectURL(new Blob([makeNote()], {type: "text/plain;charset=utf-8"}));
  const link = document.createElement("a");
  link.href = url; link.download = "private-practitioner-notes.txt";
  document.body.appendChild(link); link.click(); link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  document.getElementById("status").textContent = "Download requested. The text file is not encrypted; choose where to keep it.";
});
document.getElementById("clear-note").addEventListener("click", () => {
  for (const [id] of fields) document.getElementById(id).value = "";
  document.getElementById("preview").textContent = "";
  document.getElementById("preview-section").hidden = true;
  document.getElementById("status").textContent = "Worksheet and preview cleared. Any downloaded copies are unchanged.";
});
