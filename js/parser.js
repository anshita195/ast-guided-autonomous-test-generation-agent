const fs = require('fs');
const acorn = require('acorn');

// Get the file path from the command-line arguments
const filePath = process.argv[2];

if (!filePath) {
  console.error("Error: Please provide a file path.");
  process.exit(1);
}

try {
  const code = fs.readFileSync(filePath, 'utf8');
  const ast = acorn.parse(code, { ecmaVersion: 2020, sourceType: 'module' });

  const functions = [];

  // A simple function to walk the AST
  function walk(node) {
    if (node.type === 'FunctionDeclaration') {
      functions.push({
        name: node.id.name,
        args: node.params.map(p => p.name)
      });
    }

    for (const key in node) {
      if (node[key] && typeof node[key] === 'object') {
        if (Array.isArray(node[key])) {
          node[key].forEach(walk);
        } else {
          walk(node[key]);
        }
      }
    }
  }

  walk(ast);

  // Output the result as a JSON string
  console.log(JSON.stringify({ functions: functions }, null, 2));

} catch (error) {
  console.error("Error parsing file:", error.message);
  process.exit(1);
}