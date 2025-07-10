const { ethers, upgrades } = require("hardhat");

async function main() {
  const SFXC = await ethers.getContractFactory("SFXCToken");

  const initialSupply = ethers.utils.parseUnits("1000000000", 18); // 1B tokens

  const sfxc = await upgrades.deployProxy(
    SFXC,
    ["SELFIX Core", "SFXC", initialSupply],
    {
      initializer: "initialize",
      kind: "uups",
    }
  );

  await sfxc.deployed();
  const proxyAddress = sfxc.address;

  console.log("✅ SFXC Token deployed to:", proxyAddress);
}

main().catch((error) => {
  console.error("❌ Deployment failed:", error);
  process.exit(1);
});
