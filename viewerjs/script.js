var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(60, 1, 1, 1000);
camera.position.set(2, 2, 2);
var renderer = new THREE.WebGLRenderer({
  antialias: true
});
renderer.setClearColor(0x808080);
var canvas = renderer.domElement
document.body.appendChild(canvas);

var controls = new THREE.OrbitControls(camera, renderer.domElement);

var light = new THREE.HemisphereLight( 0x808080, 0x000000, 1 );
scene.add( light );
//   var ambientLight = new THREE.AmbientLight( 0xcccccc );
//   scene.add( ambientLight );

var loader = new THREE.GLTFLoader();
const dracoLoader = new THREE.DRACOLoader();
dracoLoader.setDecoderPath( '/draco/' );
loader.setDRACOLoader( dracoLoader );

// loader.load( 'https://threejs.org/examples/models/gltf/Horse.glb', function ( gltf ) {
// loader.load( './freecad.glb', function ( gltf ) {
loader.load( './out.glb', function ( gltf ) {
  console.log(gltf);
  //gltf.scene.position.z = -10;
  //https://stackoverflow.com/questions/52271397/centering-and-resizing-gltf-models-automatically-in-three-js
      gltf.scene.traverse( function ( child ) {
        if ( child.isMesh ) {
            child.geometry.center(); // center here
        }
    });
  gltf.scene.traverse( child => {
    if ( child.material ) child.material.metalness = 0;
  } );
  gltf.scene.scale.set(1e-2, 1e-2, 1e-2) // scale here

  scene.add( gltf.scene );

}, undefined, function ( error ) {

  console.error( error );

} );




render();

function render() {
  if (resize(renderer)) {
    camera.aspect = canvas.clientWidth / canvas.clientHeight;
    camera.updateProjectionMatrix();
  }
  renderer.render(scene, camera);
  requestAnimationFrame(render);
}

function resize(renderer) {
  const canvas = renderer.domElement;
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;
  const needResize = canvas.width !== width || canvas.height !== height;
  if (needResize) {
    renderer.setSize(width, height, false);
  }
  return needResize;
}
