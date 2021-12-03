import * as THREE from '../threejsmaster/build/three.module.js'
import { GLTFLoader } from '../threejsmaster/examples/jsm/loaders/GLTFLoader.js'
import { OrbitControls } from '../threejsmaster/examples/jsm/controls/OrbitControls.js'

var scene, camera, renderer, cube, controls, draughts, board;
 
const darkPiece = new THREE.MeshStandardMaterial( { color: 0x222222 } );
const lightPiece = new THREE.MeshStandardMaterial( { color: 0xFFFFFF });
 
function init() {
  draughts = new Draughts();
 
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
 
  renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);
 
  const square = new THREE.BoxGeometry(1, 0.1, 1);
  const lightsquare = new THREE.MeshBasicMaterial( { color: 0xE0C4A8 } );
  const darksquare = new THREE.MeshBasicMaterial( { color: 0x6A4236});
  board = new THREE.Group();
 
  const light = new THREE.PointLight( 0xffffff, 2, 200 );
  light.position.set(5, 10, 5);
  scene.add(light);
 
  let cubeNumber = 1;
 
  for (let x = 0; x < 10; x++) {
    for (let z = 0; z < 10; z++) {
      let cube;
      if (z % 2 == 0) {
        cube = new THREE.Mesh(square, x % 2 == 0 ? lightsquare : darksquare);
        if (x % 2 != 0) {
          cube.userData.cubeNumber = cubeNumber;
          cubeNumber++;
        }
      }
      else {
        cube = new THREE.Mesh(square, x % 2 == 0 ? darksquare : lightsquare);
        if (x % 2 == 0) {
          cube.userData.cubeNumber = cubeNumber;
          cubeNumber++;
        }
      }
      cube.position.set(x, 0, z);
      board.add(cube);
    }
  }
 
  scene.add(board);
 
  const loader = new GLTFLoader();
  loader.load( '../checker.glb', function ( gltf ) {
    const checkerMesh = gltf.scene.children.find((child) => child.name === "Checker");
    checkerMesh.scale.set(checkerMesh.scale.x * 0.4, checkerMesh.scale.y * 0.4, checkerMesh.scale.z * 0.4);
    checkerMesh.geometry.computeBoundingBox();
    console.log(checkerMesh.geometry.boundingBox);
    checkerMesh.position.y += checkerMesh.scale.y + 0.05;
    addCheckers(checkerMesh);
  }, undefined, function ( error ) {
 
    console.error( error );
 
  } );
 
  camera.position.y = 8;
 
  camera.position.set(4.5, 5, 4.5);
  camera.lookAt(5, 0, 5);
 
  controls = new OrbitControls(camera, renderer.domElement);
 
  controls.target.set(4.5, 0, 4.5);
  controls.enablePan = false;
  controls.maxPolarAngle = Math.PI / 2;
 
  controls.enableDamping = true;
 
  window.requestAnimationFrame(animate);
}
 
function animate() {
  controls.update();
  renderer.render(scene, camera);
  window.requestAnimationFrame(animate);
}
 
function positionForSquare(square) {
  const found = board.children.find((child) => child.userData.cubeNumber == square);
  if (found)
    return found.position;
  return null;
}
 
function addCheckers(checkerMesh) {
  console.log(draughts.fen());
 
  for (let i = 1; i < 51; i++) {
    let pieceOn = draughts.get(i);
 
    const squarePosition = positionForSquare(i);
 
    if (pieceOn === 'b') {
      const piece = checkerMesh.clone(true);
      piece.material = darkPiece;
      piece.userData.color = 'b';
      piece.userData.currentSquare = i;
      piece.position.set(squarePosition.x, piece.position.y, squarePosition.z);
      scene.add(piece);
    } else if (pieceOn === 'w') {
      const piece = checkerMesh.clone(true);
      piece.material = lightPiece;
      piece.userData.color = 'w';
      piece.userData.currentSquare = i;
      piece.position.set(squarePosition.x, piece.position.y, squarePosition.z);
      scene.add(piece);
    }
  }
}
 
function onWindowResize() {
 
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
 
  renderer.setSize( window.innerWidth, window.innerHeight );
}
 
 
window.addEventListener('resize', onWindowResize);
 
window.onload = init;