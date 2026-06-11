/**
 * Client-Side Repository Parser
 * Allows parsing local directories completely in the browser using HTML5 directory upload.
 */
class BrowserCodeParser {
    static calculateComplexity(content) {
        const branchPoints = (content.match(/\b(if|for|while|elif|else|catch|case|&&|\|\|)\b/g) || []).length;
        return Math.max(1, branchPoints + 1);
    }

    static detectBugsRisks(content, filePath) {
        const risks = [];
        
        // 1. Security Check: Hardcoded Secrets
        const secretRegex = /\b(secret|password|passwd|token|api_key|private_key)\s*=\s*['"][^'"]{4,}['"]/gi;
        let match;
        while ((match = secretRegex.exec(content)) !== null) {
            const lineNo = content.substring(0, match.index).split('\n').length;
            risks.push({
                category: "SECURITY",
                severity: "CRITICAL",
                message: "Potential hardcoded credential or secret key detected.",
                line: lineNo,
                snippet: match[0],
                owaspRef: "OWASP A02:2021-Cryptographic Failures"
            });
        }

        // 2. Security Check: eval/exec injection risk
        const dangerousRegex = /\b(eval|exec|unsafe|dangerouslySetInnerHTML)\b/g;
        while ((match = dangerousRegex.exec(content)) !== null) {
            const lineNo = content.substring(0, match.index).split('\n').length;
            const lines = content.split('\n');
            risks.push({
                category: "SECURITY",
                severity: "HIGH",
                message: `Dangerous operation '${match[1]}' used, exposing injection vulnerabilities.`,
                line: lineNo,
                snippet: lines[lineNo - 1]?.trim() || "",
                owaspRef: "OWASP A03:2021-Injection"
            });
        }

        // 3. Modularity Smell: God file
        const lines = content.split('\n');
        if (lines.length > 250) {
            risks.push({
                category: "ARCH",
                severity: "MEDIUM",
                message: `God File Smell: File contains ${lines.length} lines, violating modularity patterns.`,
                line: 1,
                snippet: lines[0] || "",
                owaspRef: "Clean Code: Single Responsibility Principle"
            });
        }

        // 4. Performance/Error handling check: empty catch blocks
        const catchRegex = /(except\b.*:|catch\s*\(.*\)\s*\{)\s*(\bpass\b|\bcontinue\b|\{\}|\s*\}|\s*\/\/\s*.*)/g;
        while ((match = catchRegex.exec(content)) !== null) {
            const lineNo = content.substring(0, match.index).split('\n').length;
            risks.push({
                category: "PERF",
                severity: "HIGH",
                message: "Silent Failure: Empty catch/except block swallows errors, preventing debugging.",
                line: lineNo,
                snippet: match[0].trim().replace(/\n/g, ' '),
                owaspRef: "OWASP A09:2021-Security Logging failures"
            });
        }

        return risks;
    }

    static parseFile(filePath, content) {
        const ext = filePath.split('.').pop().toLowerCase();
        const metrics = {
            classes: [],
            functions: [],
            dependencies: [],
            bugs: [],
            loc: content.split('\n').length,
            complexity: this.calculateComplexity(content),
            coverage: 0,
            language: "Text"
        };

        // Simulated test coverage
        if (filePath.toLowerCase().includes('test')) {
            metrics.coverage = 100;
        } else {
            // hash-like deterministic coverage
            let hash = 0;
            for (let i = 0; i < content.length; i++) {
                hash = (hash << 5) - hash + content.charCodeAt(i);
                hash |= 0;
            }
            metrics.coverage = 20 + Math.abs(hash % 76);
        }

        metrics.bugs = this.detectBugsRisks(content, filePath);

        // Language specific parsing
        if (ext === 'py') {
            metrics.language = "Python";
            
            // Classes
            const classRegex = /^\s*class\s+(\w+)(?:\s*\((.*?)\))?\s*:/gm;
            let match;
            while ((match = classRegex.exec(content)) !== null) {
                metrics.classes.push({
                    name: match[1],
                    line: content.substring(0, match.index).split('\n').length,
                    inherits: match[2] ? match[2].split(',').map(x => x.trim()) : []
                });
            }

            // Functions
            const funcRegex = /^\s*def\s+(\w+)\s*\((.*?)\)\s*(?:->\s*.*?)?:/gm;
            while ((match = funcRegex.exec(content)) !== null) {
                const paramCount = match[2] ? match[2].split(',').filter(x => x.trim()).length : 0;
                metrics.functions.push({
                    name: match[1],
                    line: content.substring(0, match.index).split('\n').length,
                    paramCount: paramCount,
                    isPublic: !match[1].startsWith('_')
                });
            }

            // Dependencies
            const depRegex = /^\s*(?:import\s+(\w+)|from\s+(\w+)\s+import)/gm;
            while ((match = depRegex.exec(content)) !== null) {
                const dep = match[1] || match[2];
                if (dep) metrics.dependencies.push(dep);
            }

        } else if (['js', 'jsx', 'ts', 'tsx'].includes(ext)) {
            metrics.language = ['js', 'jsx'].includes(ext) ? "JavaScript" : "TypeScript";

            // Classes
            const classRegex = /\bclass\s+(\w+)(?:\s+extends\s+(\w+))?/g;
            let match;
            while ((match = classRegex.exec(content)) !== null) {
                metrics.classes.push({
                    name: match[1],
                    line: content.substring(0, match.index).split('\n').length,
                    inherits: match[2] ? [match[2]] : []
                });
            }

            // Functions
            const funcRegex = /\b(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:\(.*?\)|[^=\n]+)\s*=>|(\w+)\s*\((.*?)\)\s*\{)/g;
            while ((match = funcRegex.exec(content)) !== null) {
                const name = match[1] || match[2] || match[3];
                if (name && !['if', 'for', 'while', 'switch', 'catch'].includes(name)) {
                    const params = match[4] || "";
                    const paramCount = params ? params.split(',').filter(x => x.trim()).length : 0;
                    metrics.functions.push({
                        name: name,
                        line: content.substring(0, match.index).split('\n').length,
                        paramCount: paramCount,
                        isPublic: true
                    });
                }
            }

            // Dependencies
            const depRegex = /\b(?:import\s+.*?\s+from\s+['"](.*?)['"]|require\s*\(\s*['"](.*?)['"]\s*\))/g;
            while ((match = depRegex.exec(content)) !== null) {
                const depPath = match[1] || match[2];
                if (depPath) {
                    const depName = depPath.split('/').pop();
                    metrics.dependencies.push(depName);
                }
            }

        } else if (ext === 'go') {
            metrics.language = "Go";

            // Classes (structs as class analogs)
            const structRegex = /\btype\s+(\w+)\s+struct\b/g;
            let match;
            while ((match = structRegex.exec(content)) !== null) {
                metrics.classes.push({
                    name: match[1],
                    line: content.substring(0, match.index).split('\n').length,
                    inherits: []
                });
            }

            // Functions
            const funcRegex = /\bfunc\s+(?:\((.*?)\)\s*)?(\w+)\s*\((.*?)\)/g;
            while ((match = funcRegex.exec(content)) !== null) {
                const name = match[2];
                const params = match[3] || "";
                const paramCount = params ? params.split(',').filter(x => x.trim()).length : 0;
                metrics.functions.push({
                    name: name,
                    line: content.substring(0, match.index).split('\n').length,
                    paramCount: paramCount,
                    isPublic: name ? name[0] === name[0].toUpperCase() : false
                });
            }

            // Dependencies
            const depRegex = /\bimport\s+\((.*?)\)|\bimport\s+['"](.*?)['"]/gs;
            while ((match = depRegex.exec(content)) !== null) {
                if (match[1]) {
                    const paths = match[1].match(/['"](.*?)['"]/g) || [];
                    paths.forEach(p => {
                        const cleanPath = p.replace(/['"]/g, '');
                        metrics.dependencies.push(cleanPath.split('/').pop());
                    });
                } else if (match[2]) {
                    metrics.dependencies.push(match[2].split('/').pop());
                }
            }

        } else if (ext === 'java') {
            metrics.language = "Java";

            // Classes
            const classRegex = /\b(?:class|interface|enum)\s+(\w+)/g;
            let match;
            while ((match = classRegex.exec(content)) !== null) {
                metrics.classes.push({
                    name: match[1],
                    line: content.substring(0, match.index).split('\n').length,
                    inherits: []
                });
            }

            // Functions
            const funcRegex = /\b(?:public|protected|private|static|\s)+\s+[\w<>]+\s+(\w+)\s*\((.*?)\)\s*(?:throws\s+.*?)?\{/g;
            while ((match = funcRegex.exec(content)) !== null) {
                const name = match[1];
                if (name && !['if', 'for', 'while', 'switch', 'catch', 'synchronized'].includes(name)) {
                    const params = match[2] || "";
                    const paramCount = params ? params.split(',').filter(x => x.trim()).length : 0;
                    metrics.functions.push({
                        name: name,
                        line: content.substring(0, match.index).split('\n').length,
                        paramCount: paramCount,
                        isPublic: match[0].includes('public')
                    });
                }
            }

            // Dependencies
            const depRegex = /^\s*import\s+(.*?);/gm;
            while ((match = depRegex.exec(content)) !== null) {
                metrics.dependencies.push(match[1].split('.').pop());
            }
        }

        return metrics;
    }

    static buildGalaxyGraph(filesData) {
        const nodes = [];
        const edges = [];
        const summary = {
            stars: 0,
            planets: 0,
            orbits: 0,
            blackholes: 0,
            loc: 0,
            avgCoverage: 0,
            avgComplexity: 0
        };

        const nodeMap = {};
        let totalCoverage = 0;
        let totalComplexity = 0;
        let validFilesCount = 0;

        // Pass 1: Add Stars (Classes/Files)
        for (const [filepath, data] of Object.entries(filesData)) {
            validFilesCount++;
            summary.loc += data.loc;
            totalCoverage += data.coverage;
            totalComplexity += data.complexity;

            if (data.classes.length > 0) {
                data.classes.forEach(cls => {
                    summary.stars++;
                    const nodeId = `class:${filepath}:${cls.name}`;
                    const node = {
                        id: nodeId,
                        name: cls.name,
                        type: "star",
                        filepath: filepath,
                        language: data.language,
                        loc: data.loc,
                        coverage: data.coverage,
                        complexity: data.complexity,
                        line: cls.line,
                        bugsCount: data.bugs.length,
                        workSignalsCount: Math.abs(cls.name.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0)) % 4
                    };
                    nodes.push(node);
                    nodeMap[cls.name] = nodeId;
                });
            } else {
                summary.stars++;
                const baseName = filepath.split('/').pop();
                const nodeId = `file:${filepath}:${baseName}`;
                const node = {
                    id: nodeId,
                    name: baseName,
                    type: "star",
                    filepath: filepath,
                    language: data.language,
                    loc: data.loc,
                    coverage: data.coverage,
                    complexity: data.complexity,
                    line: 1,
                    bugsCount: data.bugs.length,
                    workSignalsCount: Math.abs(baseName.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0)) % 4
                };
                nodes.push(node);
                nodeMap[baseName] = nodeId;
            }

            // Planets (Functions)
            data.functions.forEach(func => {
                summary.planets++;
                const funcId = `func:${filepath}:${func.name}`;
                const parentId = data.classes.length > 0 
                    ? `class:${filepath}:${data.classes[0].name}` 
                    : `file:${filepath}:${filepath.split('/').pop()}`;

                nodes.push({
                    id: funcId,
                    name: func.name,
                    type: "planet",
                    filepath: filepath,
                    language: data.language,
                    parentStar: parentId,
                    paramCount: func.paramCount,
                    isPublic: func.isPublic,
                    complexity: Math.max(1, Math.floor(data.complexity / (data.functions.length || 1))),
                    line: func.line
                });

                edges.push({
                    source: parentId,
                    target: funcId,
                    type: "orbit"
                });
            });

            // Black holes (Bugs)
            data.bugs.forEach(bug => {
                summary.blackholes++;
                const bugId = `bug:${filepath}:${bug.category}:${bug.line}`;
                const parentId = data.classes.length > 0 
                    ? `class:${filepath}:${data.classes[0].name}` 
                    : `file:${filepath}:${filepath.split('/').pop()}`;

                nodes.push({
                    id: bugId,
                    name: `${bug.category}: L${bug.line}`,
                    type: "blackhole",
                    filepath: filepath,
                    category: bug.category,
                    severity: bug.severity,
                    message: bug.message,
                    line: bug.line,
                    owaspRef: bug.owaspRef,
                    snippet: bug.snippet,
                    parentStar: parentId
                });

                edges.push({
                    source: parentId,
                    target: bugId,
                    type: "gravitational_pull"
                });
            });
        }

        // Pass 2: Resolve Dependencies (Orbits)
        for (const [filepath, data] of Object.entries(filesData)) {
            const parentId = data.classes.length > 0 
                ? `class:${filepath}:${data.classes[0].name}` 
                : `file:${filepath}:${filepath.split('/').pop()}`;

            data.dependencies.forEach(dep => {
                if (nodeMap[dep]) {
                    summary.orbits++;
                    edges.push({
                        source: parentId,
                        target: nodeMap[dep],
                        type: "dependency",
                        strength: 2 + (data.complexity % 4)
                    });
                }
            });
        }

        if (validFilesCount > 0) {
            summary.avgCoverage = Math.round((totalCoverage / validFilesCount) * 10) / 10;
            summary.avgComplexity = Math.round((totalComplexity / validFilesCount) * 10) / 10;
        }

        return {
            summary,
            nodes,
            edges
        };
    }
}

// Generate Work IQ contextual details client-side
class BrowserWorkIQSimulator {
    static DEVELOPERS = ["Sarah Chen", "Marcus Vance", "Elena Rostova", "Alex Mercer"];
    static MESSAGES = [
        "Hey team, this module has been failing on prod occasionally. I think there is a concurrency leak in the connection pool.",
        "Refactoring this class today to fit the new Auth spec. Ping me if you hit any import breaks.",
        "Let's add test coverage for this function before the sprint review. Fabric IQ shows it has 0% coverage currently.",
        "OWASP scan flagged this section for weak hashing. We should migrate this to PBKDF2 as soon as possible.",
        "This is deprecated code from v1. Please don't write any new imports pointing to this module.",
        "We discussed this file in the standup meeting on June 8th. The plan is to split it into microservices next sprint."
    ];

    static getSignals(nodeName, seedStr) {
        let hash = 0;
        for (let i = 0; i < seedStr.length; i++) {
            hash = (hash << 5) - hash + seedStr.charCodeAt(i);
            hash |= 0;
        }
        hash = Math.abs(hash);

        const author = this.DEVELOPERS[hash % this.DEVELOPERS.length];
        const commitsCount = 3 + (hash % 20);
        const daysAgo = hash % 30;

        const msgCount = 1 + (hash % 3);
        const teamsDiscussions = [];
        for (let i = 0; i < msgCount; i++) {
            const msgIdx = (hash + i) % this.MESSAGES.length;
            teamsDiscussions.push({
                sender: this.DEVELOPERS[(hash + i + 1) % this.DEVELOPERS.length],
                timestamp: `${daysAgo + i} days ago`,
                message: this.MESSAGES[msgIdx]
            });
        }

        return {
            author,
            commitsCount,
            lastModified: `${daysAgo} days ago`,
            teamsDiscussions,
            prComment: `Resolved PR review comment: 'Refactor ${nodeName} to prevent cyclic dependencies.'`
        };
    }
}
