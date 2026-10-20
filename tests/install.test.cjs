'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const test = require('node:test');

const cli = path.resolve(__dirname, '../bin/aether-kit.cjs');

test('installs the skill kit and preserves existing files', (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'aether-kit-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));

  const first = spawnSync(process.execPath, [cli, 'install'], { cwd: root, encoding: 'utf8' });
  assert.equal(first.status, 0, first.stderr);
  for (const file of [
    'AGENTS.md',
    '.agents/skills/aether-workflow/SKILL.md',
    '.agents/skills/aether-repository-graph-3d/assets/graph.html',
    '.claude/agents/aether_coordinator.md',
    '.codex/agents/aether_coordinator.toml',
    'scripts/render_repository_graph.py',
  ]) {
    assert.ok(fs.statSync(path.join(root, file)).isFile(), file);
  }

  const skill = path.join(root, '.agents/skills/aether-workflow/SKILL.md');
  const before = fs.readFileSync(skill, 'utf8');
  const second = spawnSync(process.execPath, [cli, 'install'], { cwd: root, encoding: 'utf8' });
  assert.equal(second.status, 1);
  assert.match(second.stderr, /Existing files would be overwritten/);
  assert.equal(fs.readFileSync(skill, 'utf8'), before);
});

test('keeps an existing AGENTS.md', (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'aether-kit-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const instructions = path.join(root, 'AGENTS.md');
  fs.writeFileSync(instructions, 'Existing project instructions\n');

  const result = spawnSync(process.execPath, [cli, 'install'], { cwd: root, encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(fs.readFileSync(instructions, 'utf8'), 'Existing project instructions\n');
});

test('packed artifact installs and runs without registry access', (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'aether-package-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const npmCli = process.env.npm_execpath;
  assert.ok(npmCli, 'npm test must provide npm_execpath');

  const packed = spawnSync(process.execPath, [npmCli, 'pack', '--pack-destination', root, '--silent'], {
    cwd: path.resolve(__dirname, '..'),
    encoding: 'utf8',
  });
  assert.equal(packed.status, 0, packed.stderr);
  const tarball = path.join(root, packed.stdout.trim());
  assert.ok(fs.statSync(tarball).isFile());

  const consumer = path.join(root, 'consumer');
  fs.mkdirSync(consumer);
  const installEnv = { ...process.env };
  for (const key of Object.keys(installEnv)) {
    if (/allow.?scripts/i.test(key)) delete installEnv[key];
  }
  const installed = spawnSync(process.execPath, [npmCli, 'install', tarball, '--prefix', consumer, '--offline', '--no-audit', '--no-fund'], {
    encoding: 'utf8',
    env: installEnv,
  });
  assert.equal(installed.status, 0, installed.stderr);
  const packageDir = path.join(consumer, 'node_modules/aether-agent-kit');
  assert.ok(fs.statSync(path.join(packageDir, 'LICENSE')).isFile());
  assert.ok(!fs.existsSync(path.join(packageDir, 'tests')));

  const target = path.join(root, 'target');
  fs.mkdirSync(target);
  const invoked = spawnSync(process.execPath, [path.join(packageDir, 'bin/aether-kit.cjs'), 'install'], {
    cwd: target,
    encoding: 'utf8',
  });
  assert.equal(invoked.status, 0, invoked.stderr);
  assert.ok(fs.statSync(path.join(target, '.agents/skills/aether-workflow/SKILL.md')).isFile());
});
