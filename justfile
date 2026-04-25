POGOBLEND_VERSION := `cat blender_manifest.toml | grep '^version..."\K[^"]+' -oP`

build-addon:
  mkdir build/{{POGOBLEND_VERSION}} -p
  blender --command extension build --source-dir ./ --output-dir build/{{POGOBLEND_VERSION}} --split-platforms

build-docs:
  POGOBLEND_VERSION={{POGOBLEND_VERSION}} sphinx-build -E -a -b html ./docs ./docs/_build/html

open-docs:
  xdg-open ./docs/_build/html/index.html

run-docs : build-docs && open-docs

python_version := "3.11"
modules := "xxhash==3.6.0 PyYAML==6.0.3"
platforms := "macosx_11_0_arm64 manylinux_2_28_x86_64 win_amd64"
download-wheels:
  for module in {{ modules }}; do \
    for platform in {{ platforms }}; do \
      pip download $module --dest ./wheels --only-binary=:all: --python-version={{ python_version }} --platform=$platform; \
    done \
  done

