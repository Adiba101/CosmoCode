/**
 * Code Constellation 3D Galaxy Renderer (Three.js)
 */
class GalaxyRenderer {
    constructor(canvasId, onNodeSelected) {
        this.canvas = document.getElementById(canvasId);
        this.onNodeSelected = onNodeSelected;
        
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        
        this.nodes = [];
        this.edges = [];
        this.graphData = null;
        
        // ThreeJS Object collections
        this.starMeshes = [];
        this.planetMeshes = [];
        this.blackholeMeshes = [];
        this.dependencyLines = [];
        this.labelSprites = [];
        this.energyPulses = [];
        this.nebulae = [];
        
        // Interaction
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        this.hoveredNode = null;
        this.selectedNode = null;
        
        // Animation
        this.clock = new THREE.Clock();
        this.targetCameraPos = null;
        this.targetCameraLookAt = null;
        this.showLabels = true;
        
        this.init();
    }
    
    init() {
        // Create Scene
        this.scene = new THREE.Scene();
        this.scene.fog = new THREE.FogExp2(0x0a0c16, 0.002);
        
        // Create Camera
        this.camera = new THREE.PerspectiveCamera(60, this.canvas.clientWidth / this.canvas.clientHeight, 0.1, 1000);
        this.camera.position.set(0, 100, 150);
        
        // Create Renderer
        this.renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            antialias: true,
            alpha: true
        });
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        
        // Add Controls
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.maxDistance = 400;
        this.controls.minDistance = 10;
        
        // Lights
        const ambientLight = new THREE.AmbientLight(0x0e1124, 0.6); // Deep space bluish ambient
        this.scene.add(ambientLight);
        
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.4);
        dirLight.position.set(50, 150, 50);
        this.scene.add(dirLight);
        
        // Galactic Core Light (Warm Golden Glow)
        const coreLight = new THREE.PointLight(0xff7a00, 3.5, 250);
        coreLight.position.set(0, 0, 0);
        this.scene.add(coreLight);
        
        // Deep Space Blue Ambient Light
        const spaceLight = new THREE.PointLight(0x0055ff, 2.0, 300);
        spaceLight.position.set(0, 80, 0);
        this.scene.add(spaceLight);

        // Warm Purple Side Light
        const sideLight = new THREE.PointLight(0xa300ff, 1.5, 300);
        sideLight.position.set(-80, -20, -80);
        this.scene.add(sideLight);
        
        // Add ambient space dust (stars)
        this.createSpaceDust();
        
        // Event Listeners
        window.addEventListener('resize', () => this.onWindowResize());
        this.canvas.addEventListener('mousemove', (e) => this.onMouseMove(e));
        this.canvas.addEventListener('click', (e) => this.onMouseClick(e));
        
        // Start Loop
        this.animate();
    }
    
    generateGlowTexture() {
        const canvas = document.createElement('canvas');
        canvas.width = 64;
        canvas.height = 64;
        const ctx = canvas.getContext('2d');
        
        const gradient = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
        gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
        gradient.addColorStop(0.18, 'rgba(240, 248, 255, 0.95)');
        gradient.addColorStop(0.45, 'rgba(128, 170, 255, 0.35)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, 64, 64);
        
        return new THREE.CanvasTexture(canvas);
    }

    generateNebulaTexture(colorStr) {
        const canvas = document.createElement('canvas');
        canvas.width = 128;
        canvas.height = 128;
        const ctx = canvas.getContext('2d');
        
        const gradient = ctx.createRadialGradient(64, 64, 0, 64, 64, 64);
        gradient.addColorStop(0, colorStr);
        gradient.addColorStop(0.45, colorStr.replace(/[\d\.]+\)$/, '0.04)'));
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, 128, 128);
        
        return new THREE.CanvasTexture(canvas);
    }

    createSpaceDust() {
        const particleCount = 4500;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const colors = new Float32Array(particleCount * 3);
        
        const arms = 3;
        const armAngle = (2 * Math.PI) / arms;
        
        for (let i = 0; i < particleCount; i++) {
            const idx = i * 3;
            
            // Distribute stars mostly in spiral arms or dense galactic core
            const isCore = Math.random() < 0.25;
            let r = 0;
            let theta = 0;
            
            if (isCore) {
                // Galactic core: dense sphere in center
                r = Math.pow(Math.random(), 2) * 15;
                theta = Math.random() * Math.PI * 2;
            } else {
                // Spiral arms: distribute along arms with scatter
                const progress = Math.random();
                r = 10 + progress * 140;
                const armIdx = Math.floor(Math.random() * arms);
                const spiralFactor = 2.2;
                const scatter = 12 / (0.4 + progress * 2.5); // scatter decreases further out
                
                theta = r * spiralFactor + (armIdx * armAngle) + (Math.random() - 0.5) * (scatter / (r + 1));
            }
            
            positions[idx] = r * Math.cos(theta);
            // Height dispersion (disk thickness)
            positions[idx + 1] = (Math.random() - 0.5) * (10 - (r / 150) * 8);
            positions[idx + 2] = r * Math.sin(theta);
            
            // Color grading: Core is warm yellow/orange/white, arms are deep blue/purple/magenta
            if (isCore) {
                colors[idx] = 0.95 + Math.random() * 0.05;     // Red
                colors[idx + 1] = 0.85 + Math.random() * 0.15; // Green
                colors[idx + 2] = 0.65 + Math.random() * 0.25; // Blue
            } else {
                const colRand = Math.random();
                if (colRand < 0.45) {
                    // Deep blue / indigo
                    colors[idx] = 0.1 + Math.random() * 0.2;
                    colors[idx + 1] = 0.2 + Math.random() * 0.3;
                    colors[idx + 2] = 0.8 + Math.random() * 0.2;
                } else if (colRand < 0.8) {
                    // Magenta / Purple
                    colors[idx] = 0.6 + Math.random() * 0.4;
                    colors[idx + 1] = 0.1 + Math.random() * 0.2;
                    colors[idx + 2] = 0.7 + Math.random() * 0.3;
                } else {
                    // Cyan / Teal
                    colors[idx] = 0.1 + Math.random() * 0.2;
                    colors[idx + 1] = 0.7 + Math.random() * 0.3;
                    colors[idx + 2] = 0.8 + Math.random() * 0.2;
                }
            }
        }
        
        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        
        // Use custom circular glow texture for beautiful star points!
        this.dustTexture = this.generateGlowTexture();
        const material = new THREE.PointsMaterial({
            size: 2.2,
            map: this.dustTexture,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        });
        
        this.spaceDust = new THREE.Points(geometry, material);
        this.scene.add(this.spaceDust);
        
        // Add large colorful nebula clouds to give volumetric depth to space!
        this.createNebulaClouds();
    }
    
    createNebulaClouds() {
        this.nebulae = [];
        const cloudCount = 10;
        this.nebulaPurpleTex = this.generateNebulaTexture('rgba(140, 30, 255, 0.15)');
        this.nebulaBlueTex = this.generateNebulaTexture('rgba(0, 100, 255, 0.15)');
        this.nebulaOrangeTex = this.generateNebulaTexture('rgba(255, 80, 0, 0.08)');
        
        const textures = [this.nebulaPurpleTex, this.nebulaBlueTex, this.nebulaOrangeTex];
        
        for (let i = 0; i < cloudCount; i++) {
            const size = 150 + Math.random() * 150;
            const geom = new THREE.PlaneGeometry(size, size);
            
            const mat = new THREE.MeshBasicMaterial({
                map: textures[i % textures.length],
                transparent: true,
                opacity: 0.4 + Math.random() * 0.4,
                blending: THREE.AdditiveBlending,
                depthWrite: false,
                side: THREE.DoubleSide
            });
            
            const mesh = new THREE.Mesh(geom, mat);
            
            const angle = Math.random() * Math.PI * 2;
            const dist = Math.random() * 80;
            mesh.position.set(
                dist * Math.cos(angle),
                (Math.random() - 0.5) * 8,
                dist * Math.sin(angle)
            );
            
            mesh.rotation.x = Math.PI / 2 + (Math.random() - 0.5) * 0.15;
            mesh.rotation.y = (Math.random() - 0.5) * 0.15;
            mesh.rotation.z = Math.random() * Math.PI * 2;
            
            this.scene.add(mesh);
            this.nebulae.push(mesh);
        }
    }
    
    // Generates coordinates along spiral galaxy arms
    getGalaxySpiralPosition(index, total) {
        const arms = 3;
        const angleOffset = (index % arms) * (2 * Math.PI / arms);
        
        // Distribute distance non-linearly (more dense in center)
        const progress = index / total;
        const radius = 10 + progress * 70;
        
        // Spiral angle
        const spiralFactor = 2.5;
        const theta = radius * spiralFactor + angleOffset;
        
        // Random scatter
        const scatter = 5;
        const x = radius * Math.cos(theta) + (Math.random() - 0.5) * scatter;
        const z = radius * Math.sin(theta) + (Math.random() - 0.5) * scatter;
        const y = (Math.random() - 0.5) * (15 - progress * 10);
        
        return new THREE.Vector3(x, y, z);
    }
    
    renderGraph(graphData) {
        this.graphData = graphData;
        this.clearGraph();
        
        const starNodes = graphData.nodes.filter(n => n.type === 'star');
        const planetNodes = graphData.nodes.filter(n => n.type === 'planet');
        const blackholeNodes = graphData.nodes.filter(n => n.type === 'blackhole');
        
        const posMap = {};
        
        // 1. Render Stars (Classes)
        starNodes.forEach((node, index) => {
            const pos = this.getGalaxySpiralPosition(index, starNodes.length);
            posMap[node.id] = pos;
            
            // Sphere scale by LOC
            const size = Math.max(1.8, Math.min(6, 1.5 + (node.loc / 120)));
            const geometry = new THREE.SphereGeometry(size, 24, 24);
            
            // Color by language
            let colorVal = 0x388bfd; // default blue
            if (node.language === "Python") colorVal = 0xd4a72c; // yellow
            else if (node.language === "Java") colorVal = 0xf85149; // red
            else if (node.language === "Go") colorVal = 0x39d353; // green
            
            const material = new THREE.MeshStandardMaterial({
                color: colorVal,
                emissive: colorVal,
                emissiveIntensity: 0.35 + (node.coverage / 100) * 0.35, // Brightness by test coverage
                roughness: 0.1,
                metalness: 0.9
            });
            
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.copy(pos);
            mesh.userData = { 
                nodeData: node,
                originalRadius: size
            };
            this.scene.add(mesh);
            this.starMeshes.push(mesh);
            
            // Star corona halo glow sprite
            const coronaTexture = this.generateGlowTexture();
            const glowMaterial = new THREE.SpriteMaterial({
                map: coronaTexture,
                color: colorVal,
                transparent: true,
                opacity: 0.8,
                blending: THREE.AdditiveBlending,
                depthWrite: false
            });
            const glowSprite = new THREE.Sprite(glowMaterial);
            glowSprite.scale.set(size * 3.8, size * 3.8, 1);
            mesh.add(glowSprite);
            mesh.userData.glowSprite = glowSprite;
            
            // Add subtle orbit boundary helper rings around class stars
            const ringGeo = new THREE.RingGeometry(size * 1.4, size * 1.5, 30);
            const ringMat = new THREE.MeshBasicMaterial({
                color: 0x388bfd,
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.06
            });
            const ring = new THREE.Mesh(ringGeo, ringMat);
            ring.rotation.x = Math.PI / 2;
            mesh.add(ring);
            
            // Add custom particle halo glow if risk score is low / clean code
            if (node.bugsCount === 0) {
                const haloGeo = new THREE.SphereGeometry(size * 1.25, 16, 16);
                const haloMat = new THREE.MeshBasicMaterial({
                    color: 0x39d353,
                    transparent: true,
                    opacity: 0.12,
                    wireframe: true
                });
                const halo = new THREE.Mesh(haloGeo, haloMat);
                mesh.add(halo);
            }
            
            // Generate node label sprite
            this.createNodeLabel(mesh, node.name, colorVal);
        });
        
        // 2. Render Planets (Functions)
        planetNodes.forEach((node, index) => {
            const parentPos = posMap[node.parentStar];
            if (!parentPos) return;
            
            // Size by param count (more parameters = rings/bigger planet)
            const size = 0.5 + (node.paramCount * 0.15);
            const geometry = new THREE.SphereGeometry(size, 12, 12);
            
            const colorVal = 0x8957e5; // Purple functions
            const material = new THREE.MeshStandardMaterial({
                color: colorVal,
                emissive: colorVal,
                emissiveIntensity: 0.1,
                roughness: 0.3
            });
            
            const mesh = new THREE.Mesh(geometry, material);
            mesh.userData = { 
                nodeData: node,
                parentPos: parentPos,
                orbitRadius: 6 + (index % 4) * 2, // staggered orbits
                angle: Math.random() * Math.PI * 2,
                orbitSpeed: 0.005 + (0.02 / node.complexity) // more complex functions rotate slower
            };
            
            // Set initial position
            mesh.position.set(
                parentPos.x + mesh.userData.orbitRadius * Math.cos(mesh.userData.angle),
                parentPos.y,
                parentPos.z + mesh.userData.orbitRadius * Math.sin(mesh.userData.angle)
            );
            
            this.scene.add(mesh);
            this.planetMeshes.push(mesh);
            
            // Add glowing atmosphere sprite for planets
            const planetGlow = new THREE.Sprite(new THREE.SpriteMaterial({
                map: this.generateGlowTexture(),
                color: colorVal,
                transparent: true,
                opacity: 0.6,
                blending: THREE.AdditiveBlending,
                depthWrite: false
            }));
            planetGlow.scale.set(size * 3.5, size * 3.5, 1);
            mesh.add(planetGlow);
            
            // Add function orbits as a delicate glowing LineLoop
            const orbitPoints = [];
            const segments = 64;
            for (let j = 0; j <= segments; j++) {
                const theta = (j / segments) * Math.PI * 2;
                orbitPoints.push(new THREE.Vector3(
                    mesh.userData.orbitRadius * Math.cos(theta),
                    0,
                    mesh.userData.orbitRadius * Math.sin(theta)
                ));
            }
            const orbitGeo = new THREE.BufferGeometry().setFromPoints(orbitPoints);
            const orbitMat = new THREE.LineBasicMaterial({
                color: 0x8957e5,
                transparent: true,
                opacity: 0.16,
                blending: THREE.AdditiveBlending
            });
            const orbit = new THREE.LineLoop(orbitGeo, orbitMat);
            orbit.position.copy(parentPos);
            this.scene.add(orbit);
            this.dependencyLines.push(orbit);
            
            // If function is complex and has high arguments, give it a tiny planetary ring
            if (node.paramCount > 2) {
                const ringGeo = new THREE.RingGeometry(size * 1.4, size * 1.9, 15);
                const ringMat = new THREE.MeshBasicMaterial({
                    color: 0xd4a72c,
                    side: THREE.DoubleSide,
                    transparent: true,
                    opacity: 0.3,
                    blending: THREE.AdditiveBlending
                });
                const ring = new THREE.Mesh(ringGeo, ringMat);
                ring.rotation.x = Math.PI / 3;
                mesh.add(ring);
            }
        });
        
        // 3. Render Black Holes (Bugs)
        blackholeNodes.forEach((node, index) => {
            const parentPos = posMap[node.parentStar];
            if (!parentPos) return;
            
            // Position close to parent star
            const angle = (index * 1.5) % (Math.PI * 2);
            const radius = 8 + (index % 3) * 2;
            const pos = new THREE.Vector3(
                parentPos.x + radius * Math.cos(angle),
                parentPos.y + (Math.random() - 0.5) * 4,
                parentPos.z + radius * Math.sin(angle)
            );
            
            // Inner event horizon (dark sphere)
            const eventHorizonSize = node.severity === 'CRITICAL' ? 1.8 : 1.2;
            const innerGeo = new THREE.SphereGeometry(eventHorizonSize, 16, 16);
            const innerMat = new THREE.MeshBasicMaterial({ color: 0x000000 });
            const innerMesh = new THREE.Mesh(innerGeo, innerMat);
            innerMesh.position.copy(pos);
            innerMesh.userData = { nodeData: node };
            this.scene.add(innerMesh);
            this.blackholeMeshes.push(innerMesh);
            
            // Accretion disk (dynamic particle accretion)
            const diskColor = node.severity === 'CRITICAL' ? 0xf85149 : 0xd4a72c;
            
            const particleCount = 180;
            const diskGeo = new THREE.BufferGeometry();
            const diskPositions = new Float32Array(particleCount * 3);
            const diskColors = new Float32Array(particleCount * 3);
            const diskParticlesData = [];
            
            const baseColor = new THREE.Color(diskColor);
            
            for (let j = 0; j < particleCount; j++) {
                const pIdx = j * 3;
                const r = eventHorizonSize * 1.6 + Math.random() * (eventHorizonSize * 2.4);
                const angle = Math.random() * Math.PI * 2;
                
                diskPositions[pIdx] = r * Math.cos(angle);
                diskPositions[pIdx + 1] = (Math.random() - 0.5) * 0.5;
                diskPositions[pIdx + 2] = r * Math.sin(angle);
                
                // Color variation: Core of disk is yellow/white, outer is red/orange
                const tempColor = baseColor.clone();
                if (Math.random() > 0.5) {
                    tempColor.addScalar(0.25); // brighter
                }
                diskColors[pIdx] = tempColor.r;
                diskColors[pIdx + 1] = tempColor.g;
                diskColors[pIdx + 2] = tempColor.b;
                
                diskParticlesData.push({
                    radius: r,
                    angle: angle,
                    speed: 0.015 + Math.random() * 0.025,
                    yVar: diskPositions[pIdx + 1]
                });
            }
            diskGeo.setAttribute('position', new THREE.BufferAttribute(diskPositions, 3));
            diskGeo.setAttribute('color', new THREE.BufferAttribute(diskColors, 3));
            
            this.blackholeDiskTexture = this.generateGlowTexture();
            const diskMat = new THREE.PointsMaterial({
                size: 0.9,
                map: this.blackholeDiskTexture,
                vertexColors: true,
                transparent: true,
                opacity: 0.9,
                blending: THREE.AdditiveBlending,
                depthWrite: false
            });
            
            const diskMesh = new THREE.Points(diskGeo, diskMat);
            diskMesh.userData = { particles: diskParticlesData };
            diskMesh.rotation.x = 0.15; // slightly tilted plane
            innerMesh.add(diskMesh);
            
            // Pulsing scale factor stored in userData
            innerMesh.userData.pulseDirection = 1;
            innerMesh.userData.originalScale = eventHorizonSize;
            
            // Visual gravitational pull lines connecting star to black hole
            const points = [parentPos, pos];
            const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
            const lineMat = new THREE.LineDashedMaterial({
                color: 0xf85149,
                dashSize: 1,
                gapSize: 1.5,
                transparent: true,
                opacity: 0.3
            });
            const line = new THREE.Line(lineGeo, lineMat);
            line.computeLineDistances();
            this.scene.add(line);
            this.dependencyLines.push(line);
        });
        
        // 4. Render Dependency Links (Orbits/Edges) and flowing energy pulses
        graphData.edges.filter(e => e.type === 'dependency').forEach(edge => {
            const startPos = posMap[edge.source];
            const endPos = posMap[edge.target];
            if (!startPos || !endPos) return;
            
            // Create nice bezier/quadratic curves for connection pathways
            const midX = (startPos.x + endPos.x) / 2;
            const midY = Math.max(startPos.y, endPos.y) + 12; // arch curve upwards
            const midZ = (startPos.z + endPos.z) / 2;
            const controlPoint = new THREE.Vector3(midX, midY, midZ);
            
            const curve = new THREE.QuadraticBezierCurve3(startPos, controlPoint, endPos);
            const points = curve.getPoints(32);
            const geometry = new THREE.BufferGeometry().setFromPoints(points);
            
            // Color based on coupling weight strength
            const colorVal = edge.strength && edge.strength > 4 ? 0xf85149 : 0x388bfd;
            
            const material = new THREE.LineBasicMaterial({
                color: colorVal,
                transparent: true,
                opacity: 0.2,
                linewidth: edge.strength || 1,
                blending: THREE.AdditiveBlending
            });
            
            const line = new THREE.Line(geometry, material);
            this.scene.add(line);
            this.dependencyLines.push(line);
            
            // Spawn an energy pulse along the dependency line
            const pulseGeom = new THREE.BufferGeometry();
            pulseGeom.setAttribute('position', new THREE.BufferAttribute(new Float32Array([startPos.x, startPos.y, startPos.z]), 3));
            
            this.pulseTexture = this.generateGlowTexture();
            const pulseMat = new THREE.PointsMaterial({
                color: colorVal,
                size: 2.5,
                map: this.pulseTexture,
                transparent: true,
                opacity: 1.0,
                blending: THREE.AdditiveBlending,
                depthWrite: false
            });
            
            const pulseMesh = new THREE.Points(pulseGeom, pulseMat);
            this.scene.add(pulseMesh);
            
            this.energyPulses.push({
                mesh: pulseMesh,
                curve: curve,
                progress: Math.random(), // randomize starting position to distribute flow
                speed: 0.08 + Math.random() * 0.12
            });
        });
    }
    
    // Renders custom HTML tags as canvas sprites
    createNodeLabel(mesh, text, colorHex) {
        const canvas = document.createElement('canvas');
        canvas.width = 128;
        canvas.height = 32;
        const ctx = canvas.getContext('2d');
        
        // Draw text with subtle shadow
        ctx.fillStyle = 'rgba(10, 12, 22, 0.6)';
        ctx.fillRect(0, 0, 128, 32);
        
        ctx.font = 'bold 16px Outfit, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        
        // Text Shadow
        ctx.fillStyle = '#000';
        ctx.fillText(text, 65, 17);
        
        // Text Color matching language
        ctx.fillStyle = '#' + colorHex.toString(16).padStart(6, '0');
        ctx.fillText(text, 64, 16);
        
        const texture = new THREE.CanvasTexture(canvas);
        const material = new THREE.SpriteMaterial({ 
            map: texture, 
            transparent: true,
            opacity: 0.85
        });
        
        const sprite = new THREE.Sprite(material);
        sprite.scale.set(6, 1.5, 1);
        sprite.position.set(0, mesh.geometry.parameters.radius + 1.8, 0);
        
        mesh.add(sprite);
        this.labelSprites.push(sprite);
    }
    
    clearGraph() {
        // Remove Meshes and dispose of their assets to prevent memory leaks
        this.starMeshes.forEach(m => {
            if (m.userData.glowSprite) {
                m.remove(m.userData.glowSprite);
                m.userData.glowSprite.material.dispose();
            }
            this.scene.remove(m);
            m.geometry.dispose();
            if (Array.isArray(m.material)) m.material.forEach(mat => mat.dispose());
            else m.material.dispose();
        });
        
        this.planetMeshes.forEach(m => {
            this.scene.remove(m);
            m.geometry.dispose();
            m.material.dispose();
        });
        
        this.blackholeMeshes.forEach(m => {
            if (m.children.length > 0) {
                const disk = m.children[0];
                m.remove(disk);
                disk.geometry.dispose();
                disk.material.dispose();
            }
            this.scene.remove(m);
            m.geometry.dispose();
            m.material.dispose();
        });
        
        this.dependencyLines.forEach(l => {
            this.scene.remove(l);
            l.geometry.dispose();
            l.material.dispose();
        });
        
        this.energyPulses.forEach(p => {
            this.scene.remove(p.mesh);
            p.mesh.geometry.dispose();
            p.mesh.material.dispose();
        });
        
        this.starMeshes = [];
        this.planetMeshes = [];
        this.blackholeMeshes = [];
        this.dependencyLines = [];
        this.energyPulses = [];
        this.labelSprites = [];
        
        this.hoveredNode = null;
        this.selectedNode = null;
    }
    
    toggleLabels(show) {
        this.showLabels = show;
        this.labelSprites.forEach(sprite => {
            sprite.visible = show;
        });
    }
    
    // Zoom and align camera to target node ID
    focusNode(nodeId) {
        let targetMesh = null;
        const allMeshes = [...this.starMeshes, ...this.planetMeshes, ...this.blackholeMeshes];
        
        for (let mesh of allMeshes) {
            if (mesh.userData.nodeData && mesh.userData.nodeData.id === nodeId) {
                targetMesh = mesh;
                break;
            }
        }
        
        if (!targetMesh) return;
        
        // Save selected node reference
        this.selectedNode = targetMesh;
        
        // Compute world position
        const targetWorldPos = new THREE.Vector3();
        targetMesh.getWorldPosition(targetWorldPos);
        
        // Interpolate camera positioning
        this.targetCameraLookAt = targetWorldPos.clone();
        
        // Calculate camera offsets based on item type
        const type = targetMesh.userData.nodeData.type;
        const offsetDist = type === 'star' ? 25 : type === 'planet' ? 8 : 12;
        
        this.targetCameraPos = new THREE.Vector3(
            targetWorldPos.x + offsetDist,
            targetWorldPos.y + offsetDist * 0.7,
            targetWorldPos.z + offsetDist
        );
        
        // Callback UI update
        if (this.onNodeSelected) {
            this.onNodeSelected(targetMesh.userData.nodeData);
        }
        
        // Visual pulses
        this.triggerGlowPulse(targetMesh);
    }
    
    triggerGlowPulse(mesh) {
        // Temporary glowing ring animation
        const geo = new THREE.RingGeometry(0.1, 4, 30);
        const mat = new THREE.MeshBasicMaterial({
            color: 0x388bfd,
            side: THREE.DoubleSide,
            transparent: true,
            opacity: 0.8
        });
        const pulseRing = new THREE.Mesh(geo, mat);
        pulseRing.rotation.x = Math.PI / 2;
        mesh.add(pulseRing);
        
        let scaleVal = 0.1;
        const interval = setInterval(() => {
            scaleVal += 0.2;
            pulseRing.scale.set(scaleVal, scaleVal, scaleVal);
            pulseRing.material.opacity -= 0.04;
            
            if (pulseRing.material.opacity <= 0) {
                clearInterval(interval);
                mesh.remove(pulseRing);
                geo.dispose();
                mat.dispose();
            }
        }, 16);
    }
    
    // Run real-time query highlighting
    applyQueryFilter(queryStr) {
        if (!this.graphData) return;
        
        // Parse simple inputs like "complexity > 10", "coverage < 50", "type = star"
        let filterFunc = () => true; // default highlight all
        
        if (queryStr.trim()) {
            try {
                const parts = queryStr.split(/(>=|<=|>|<|=)/);
                if (parts.length >= 3) {
                    const key = parts[0].trim().toLowerCase();
                    const op = parts[1].trim();
                    const val = parseFloat(parts[2].trim()) || parts[2].trim().replace(/['"]/g, '');
                    
                    filterFunc = (node) => {
                        const nodeVal = node[key];
                        if (nodeVal === undefined) return false;
                        
                        if (op === '>') return nodeVal > val;
                        if (op === '<') return nodeVal < val;
                        if (op === '>=') return nodeVal >= val;
                        if (op === '<=') return nodeVal <= val;
                        if (op === '=') return nodeVal.toString().toLowerCase() === val.toString().toLowerCase();
                        return false;
                    };
                } else {
                    // Match by name substring
                    const term = queryStr.toLowerCase();
                    filterFunc = (node) => node.name.toLowerCase().includes(term);
                }
            } catch (e) {
                console.warn("Invalid query string syntax", e);
            }
        }
        
        // Apply opacity alterations to meshes
        const allMeshes = [...this.starMeshes, ...this.planetMeshes, ...this.blackholeMeshes];
        allMeshes.forEach(mesh => {
            const node = mesh.userData.nodeData;
            if (!node) return;
            
            const match = filterFunc(node);
            
            if (match) {
                mesh.material.opacity = 1;
                mesh.scale.set(1, 1, 1);
                if (mesh.material.emissiveIntensity !== undefined) {
                    mesh.material.emissiveIntensity = 0.4;
                }
            } else {
                mesh.material.opacity = 0.15;
                mesh.scale.set(0.7, 0.7, 0.7);
                if (mesh.material.emissiveIntensity !== undefined) {
                    mesh.material.emissiveIntensity = 0.02;
                }
            }
        });
    }
    
    onWindowResize() {
        this.camera.aspect = this.canvas.clientWidth / this.canvas.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
    }
    
    onMouseMove(event) {
        // Calculate mouse position in normalized device coordinates
        const rect = this.renderer.domElement.getBoundingClientRect();
        this.mouse.x = ((event.clientX - rect.left) / this.canvas.clientWidth) * 2 - 1;
        this.mouse.y = -((event.clientY - rect.top) / this.canvas.clientHeight) * 2 + 1;
    }
    
    onMouseClick(event) {
        this.raycaster.setFromCamera(this.mouse, this.camera);
        const allMeshes = [...this.starMeshes, ...this.planetMeshes, ...this.blackholeMeshes];
        const intersects = this.raycaster.intersectObjects(allMeshes);
        
        if (intersects.length > 0) {
            const nodeData = intersects[0].object.userData.nodeData;
            if (nodeData) {
                this.focusNode(nodeData.id);
            }
        }
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        const delta = this.clock.getDelta();
        const elapsed = this.clock.getElapsedTime();
        
        // 1. Move Planets in orbit and spin them
        this.planetMeshes.forEach(mesh => {
            mesh.userData.angle += mesh.userData.orbitSpeed;
            mesh.position.x = mesh.userData.parentPos.x + mesh.userData.orbitRadius * Math.cos(mesh.userData.angle);
            mesh.position.z = mesh.userData.parentPos.z + mesh.userData.orbitRadius * Math.sin(mesh.userData.angle);
            
            mesh.rotation.y += 0.01;
        });
        
        // 2. Spin stars slightly and pulse corona halo scales
        this.starMeshes.forEach(mesh => {
            mesh.rotation.y += 0.003;
            
            if (mesh.userData.glowSprite) {
                const pulse = 1.0 + Math.sin(elapsed * 2.5 + mesh.position.x * 0.05) * 0.12;
                const rad = mesh.userData.originalRadius;
                mesh.userData.glowSprite.scale.set(rad * 3.8 * pulse, rad * 3.8 * pulse, 1);
            }
        });
        
        // 3. Pulse Black Holes event horizon and swirl accretion disk particles
        this.blackholeMeshes.forEach(mesh => {
            const scale = mesh.userData.originalScale + Math.sin(elapsed * 4.0) * 0.12;
            mesh.scale.set(scale, scale, scale);
            
            if (mesh.children.length > 0) {
                const disk = mesh.children[0];
                if (disk.userData && disk.userData.particles) {
                    const posAttr = disk.geometry.attributes.position;
                    const parts = disk.userData.particles;
                    
                    for (let j = 0; j < parts.length; j++) {
                        const pIdx = j * 3;
                        const p = parts[j];
                        p.angle += p.speed; // Orbit speed
                        
                        posAttr.array[pIdx] = p.radius * Math.cos(p.angle);
                        posAttr.array[pIdx + 1] = p.yVar + Math.sin(elapsed * 3.0 + p.radius) * 0.08;
                        posAttr.array[pIdx + 2] = p.radius * Math.sin(p.angle);
                    }
                    posAttr.needsUpdate = true;
                }
            }
        });
        
        // 4. Update energy pulses along dependency paths
        this.energyPulses.forEach(pulse => {
            pulse.progress += delta * pulse.speed;
            if (pulse.progress > 1.0) {
                pulse.progress = 0.0;
            }
            const pos = pulse.curve.getPointAt(pulse.progress);
            const posAttr = pulse.mesh.geometry.attributes.position;
            posAttr.array[0] = pos.x;
            posAttr.array[1] = pos.y;
            posAttr.array[2] = pos.z;
            posAttr.needsUpdate = true;
        });
        
        // 5. Twinkle background stars and swirl nebula gas
        if (this.spaceDust) {
            this.spaceDust.material.opacity = 0.55 + Math.sin(elapsed * 1.8) * 0.2;
            this.spaceDust.rotation.y = elapsed * 0.015; // extremely slow galactic rotation
        }
        
        if (this.nebulae) {
            this.nebulae.forEach((mesh, idx) => {
                // slow independent rotation of gas clouds
                mesh.rotation.z += delta * 0.005 * (idx % 2 === 0 ? 1 : -1);
            });
        }
        
        // 6. Hover Raycaster highlighting
        this.raycaster.setFromCamera(this.mouse, this.camera);
        const allMeshes = [...this.starMeshes, ...this.planetMeshes, ...this.blackholeMeshes];
        const intersects = this.raycaster.intersectObjects(allMeshes);
        
        if (intersects.length > 0) {
            const obj = intersects[0].object;
            if (this.hoveredNode !== obj) {
                if (this.hoveredNode && this.hoveredNode.material.emissiveIntensity !== undefined) {
                    this.hoveredNode.material.emissiveIntensity = this.hoveredNode.userData.oldEmissive || 0.15;
                }
                
                this.hoveredNode = obj;
                document.body.style.cursor = 'pointer';
                
                if (obj.material.emissiveIntensity !== undefined) {
                    obj.userData.oldEmissive = obj.material.emissiveIntensity;
                    obj.material.emissiveIntensity = 0.95; // shine very bright on hover
                }
            }
        } else {
            if (this.hoveredNode) {
                if (this.hoveredNode.material.emissiveIntensity !== undefined) {
                    this.hoveredNode.material.emissiveIntensity = this.hoveredNode.userData.oldEmissive || 0.15;
                }
                this.hoveredNode = null;
                document.body.style.cursor = 'default';
            }
        }
        
        // 7. Smooth Camera Lerping
        if (this.targetCameraPos) {
            this.camera.position.lerp(this.targetCameraPos, 0.05);
            this.controls.target.lerp(this.targetCameraLookAt, 0.05);
            
            // stop lerp when close enough
            if (this.camera.position.distanceTo(this.targetCameraPos) < 0.2) {
                this.targetCameraPos = null;
                this.targetCameraLookAt = null;
            }
        }
        
        // Update Controls & Render
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }
}
