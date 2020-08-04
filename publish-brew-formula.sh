# Generate formula
pip install homebrew-pypi-poet==0.10.0 requests==2.24.0

# Code to wait till the latest package is available in pypi
cat << EOF > wait-till-publish.py
import requests
import json
import os
import time

try:
    from packaging.version import parse
except ImportError:
    from pip._vendor.packaging.version import parse

URL_PATTERN = 'https://pypi.python.org/pypi/{package}/json'


def get_version(package, url_pattern=URL_PATTERN):
    """Return version of package on pypi.python.org using json."""
    req = requests.get(url_pattern.format(package=package))
    version = parse('0')
    if req.status_code == requests.codes.ok:
        j = json.loads(req.text.encode('utf-8'))
        releases = j.get('releases', [])
        for release in releases:
            ver = parse(release)
            if not ver.is_prerelease:
                version = max(version, ver)
    return version


if __name__ == '__main__':
    tag = os.getenv('TRAVIS_TAG')
    flag = True
    while flag:
        version = get_version('socli')
        if version.base_version == tag:
            print('Got latest version from pypi, version:' + version.base_version)
            flag = False
        else:
            print('Cant get version ' + tag + ' from pypi, got: ' + version.base_version + ', Retrying in 5 secs...')
            time.sleep(5)
EOF
python wait-till-publish.py

# When latest version of socli is available in pypi do install
pip install  --no-cache socli==${TRAVIS_TAG}
# Generate formula
poet -f socli > socli.rb
patch socli.rb formula-changes.patch
echo "Generated formula:"
echo "------------------------------------------------------------------------------------"
cat socli.rb
echo ""
echo "------------------------------------------------------------------------------------"
# Pushing to tap
git config --global user.email "gkr@tuta.io"
git config --global user.name "gkr-bot"
echo "Pulling repo..."
git clone https://${BREW_GH_TOKEN}@github.com/gautamkrishnar/homebrew-socli.git brewroot > /dev/null 2>&1
echo "Generating formula..."
cp -fv socli.rb brewroot/Formula
cd brewroot
git add --all
echo "Committing formula..."
git commit -m "Published ${TRAVIS_TAG}"
echo "Pushing formula..."
git push --quiet