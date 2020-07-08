# Generate formula
pip install homebrew-pypi-poet
poet -f socli | sed "s|Shiny new formula|Stack overflow command line client. Search and browse stack overflow without leaving the terminal|g" > socli.rb
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