#!/usr/bin/env node
'use strict';

const fs = require('node:fs');
const path = require('node:path');

const packageRoot = path.resolve(__dirname, '..');
const installedPaths = [
  '.agents/skills',
  '.claude/agents',
  '.claude/skills',
  '.codex/agents',
  'scripts/render_repository_graph.py',
];
const skippedDirectories = new Set(['__pycache__', 'node_modules']);

function collectFiles(relativePath) {
  const source = path.join(packageRoot, relativePath);
  const info = fs.lstatSync(source);
  if (info.isSymbolicLink()) throw new Error(`Package contains a symlink: ${relativePath}`);
  if (info.isFile()) return [relativePath];
  if (!info.isDirectory()) throw new Error(`Unsupported package entry: ${relativePath}`);
  return fs.readdirSync(source).flatMap((name) => {
    if (skippedDirectories.has(name)) return [];
    const child = path.join(relativePath, name);
    if (fs.lstatSync(path.join(packageRoot, child)).isFile() && name.endsWith('.pyc')) return [];
    return collectFiles(child);
  });
}

function checkDestination(root, relativePath) {
  let current = root;
  const parts = relativePath.split(path.sep);
  for (let index = 0; index < parts.length; index += 1) {
    const part = parts[index];
    current = path.join(current, part);
    if (!fs.existsSync(current)) continue;
    const info = fs.lstatSync(current);
    if (info.isSymbolicLink()) {
      throw new Error(`Destination contains a symlink: ${current}`);
    }
    if (index < parts.length - 1 && !info.isDirectory()) {
      throw new Error(`Destination directory is a file: ${current}`);
    }
  }
}

function install(root) {
  const files = installedPaths.flatMap(collectFiles);
  const conflicts = [];
  for (const relativePath of files) {
    checkDestination(root, relativePath);
    if (fs.existsSync(path.join(root, relativePath))) conflicts.push(relativePath);
  }
  if (conflicts.length) {
    throw new Error(`Existing files would be overwritten:\n${conflicts.join('\n')}`);
  }
  for (const relativePath of files) {
    const destination = path.join(root, relativePath);
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    fs.copyFileSync(path.join(packageRoot, relativePath), destination, fs.constants.COPYFILE_EXCL);
  }
  const agentInstructions = path.join(root, 'AGENTS.md');
  if (!fs.existsSync(agentInstructions)) {
    fs.copyFileSync(path.join(packageRoot, 'AGENTS.md'), agentInstructions, fs.constants.COPYFILE_EXCL);
    console.log('Created AGENTS.md.');
  } else {
    console.log('Kept existing AGENTS.md. Add an Aether skill reference there if needed.');
  }
  console.log(`Installed ${files.length} Aether files in ${root}`);
}

function main() {
  const command = process.argv[2];
  if (command === '--help' || command === '-h' || command === 'help') {
    console.log('Usage: aether-kit install\n\nInstall Aether skills and agents in the current directory. Existing files are preserved.');
    return;
  }
  if (command !== 'install' || process.argv.length !== 3) {
    console.error('Usage: aether-kit install');
    process.exitCode = 2;
    return;
  }
  try {
    install(process.cwd());
  } catch (error) {
    console.error(`Aether install failed: ${error.message}`);
    process.exitCode = 1;
  }
}

main();
