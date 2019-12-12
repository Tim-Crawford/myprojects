<html>
	<head>
		<title>Minecraft Database</title>
		<link rel="shortcut icon" href="http://localhost/minecraft_interface/files/grass.ico" type="image/x-icon"/>
	</head>
	<body>
		<style>
			body {
				background-image: url(/minecraft_interface/files/dirt.png);
				background-size: 64px 64px;
				background-repeat: repeat;
				cursor: url(/minecraft_interface/files/mcmouse.png), default;
				image-rendering: pixelated;
			}
			table {
				background-image: url(/minecraft_interface/files/quartz_block_bottom.png);
				background-size: 64px 64px;
				background-repeat: repeat;
				image-rendering: pixelated;
			}
		</style>
		<table cellpadding="20">
			<tr>
				<td>
					<h1><b>Function List</b></h1>
				</td>
				<td>
					<h1><b>Input</b></h1>
				</td>
			</tr>
			<tr>
				<td valign="top">
					<h2>Items</h2>
					<a href="listitems.php">List All Items</a><br />
					<a href="iteminfo.php">Item Info</a><br />
					<a href="itemswithmostdurability.php">Items with Most Durability</a><br />
					<a href="itemswithleastdurability.php">Items with Least Durability</a><br />
					<a href="itemswithspecificdurability.php">Items with Specific Durability</a><br />
					<a href="renewableitems.php">Renewable Items</a><br />
					<a href="nonrenewableitems.php">Nonrenewable Items</a><br />
					<br />
					<h2>Blocks</h2>
					<a href="listblocks.php">List All Blocks</a><br />
					<a href="blockinfo.php">Block Info</a><br />
					<a href="blocksdrops.php">Block's Drops</a><br />
					<a href="flammableblocks.php">Flammable Blocks</a><br />
					<a href="fireproofblocks.php">Fireproof Blocks</a><br />
					<a href="tileentities.php">Tile Entities</a><br />
					<a href="tooltoharvestblock.php">Tool to Harvest Block</a><br />
					<a href="blockswithinventories.php">Blocks with Inventories</a><br />
					<a href="blocksaffectedbyfortune.php">Blocks Affected by Fortune</a><br />
					<a href="blocksaffectedbysilktouch.php">Blocks Affected by Silk Touch</a><br />
					<br />
					<h2>Entities</h2>
					<a href="listentities.php">List All Entities</a><br />
					<a href="livingentities.php">Living Entities</a><br />
					<a href="nonlivingentities.php">Nonliving Entities</a><br />
					<a href="hostileentities.php">Hostile Entities</a><br />
					<a href="passiveentities.php">Passive Entities</a><br />
					<a href="entityinfo.php">Entity Info</a><br />
					<a href="mobsdrops.php">Mob's Drops</a><br />
					<a href="entityequipment.php">Entity Equipment</a><br />
					<a href="strongestentities.php">Strongest Entities</a><br />
					<a href="weakestentities.php">Weakest Entities</a><br />
					<a href="entitieswithspecificttack.php">Entities with Specific Attack</a><br />
					<a href="entitieswithmosthp.php">Entities with Most HP</a><br />
					<a href="entitieswithleasthp.php">Entities with Least HP</a><br />
					<a href="entitieswithspecifichp.php">Entities with Specific HP</a><br />
					<a href="itemtobreedmob.php">Item to Breed Mob</a><br />
					<br />
					<h2>Enchantments</h2>
					<a href="listenchantments.php">List All Enchantments</a><br />
					<a href="findenchantsforitem.php">Find Enchants for Item</a><br />
					<a href="finditemsforenchant.php">Find Items for Enchant</a><br />
					<a href="mobsthatuseenchantment.php">Mobs that use Enchantment</a><br />
					<br />
					<h2>Status Effects</h2>
					<a href="liststatuseffects.php">List All Status Effects</a><br />
					<a href="effectorigin.php">Effect Origin</a><br />
					<a href="itemsthatgiveeffects.php">Items that give Effects</a><br />
					<a href="blocksthatgiveeffects.php">Blocks that give Effects</a><br />
					<a href="entitiesthatgiveeffects.php">Entities that give Effects</a><br />
					<br />
					<h2>Recipes</h2>
					<a href="listrecipes.php">List All Recipes</a><br />
					<a href="itemrecipes.php">Item Recipes</a><br />
					<a href="recipesthatuseitem.php">Recipes that use Item</a><br />
					<a href="tbtrecipes.php">2x2 Recipes</a><br />
					<a href="shapedrecipes.php">Shaped Recipes</a><br />
					<a href="shapelessrecipes.php">Shapeless Recipes</a><br />
					<br />
					<h2>Modify</h2>
					<h3>Insert</h3>
					<a href="insertitem.php">Insert Item into Database</a><br />
					<a href="insertblock.php">Insert Block into Database</a><br />
					<a href="insertentity.php">Insert Entity into Database</a><br />
					<a href="insertenchantment.php">Insert Enchantment into Database</a><br />
					<a href="insertstatuseffect.php">Insert Status Effect into Database</a><br />
					<a href="insertcraftingrecipe.php">Insert Crafting Recipe into Database</a><br />
					<a href="insertsmeltingrecipe.php">Insert Smelting Recipe into Database</a><br />
					<a href="insertbrewingrecipe.php">Insert Brewing Recipe into Database</a><br />
					<a href="insertitemenchant.php">Insert Item Enchant into Database</a><br />
					<a href="insertblockdrop.php">Insert Block Drop into Database</a><br />
					<a href="insertharvesttool.php">Insert Harvest Tool into Database</a><br />
					<a href="insertitemeffect.php">Insert Item Effect into Database</a><br />
					<a href="insertblockeffect.php">Insert Block Effect into Database</a><br />
					<a href="insertentityeffect.php">Insert Entity Effect into Database</a><br />
					<a href="insertentitydrop.php">Insert Entity Drop into Database</a><br />
					<a href="insertitementitycanequip.php">Insert Item Entity Can Equip into Database</a><br />
					<a href="insertitementitybreedswith.php">Insert Item Entity Breeds With into Database</a><br />
					<h3>Delete</h3>
					<a href="deleteitem.php">Delete Item from Database</a><br />
					<a href="deleteblock.php">Delete Block from Database</a><br />
					<a href="deleteentity.php">Delete Entity from Database</a><br />
					<a href="deleteenchantment.php">Delete Enchantment from Database</a><br />
					<a href="deletestatuseffect.php">Delete Status Effect from Database</a><br />
					<a href="deletecraftingrecipe.php">Delete Crafting Recipe from Database</a><br />
					<a href="deletesmeltingrecipe.php">Delete Smelting Recipe from Database</a><br />
					<a href="deletebrewingrecipe.php">Delete Brewing Recipe from Database</a><br />
					<a href="deleteitemenchant.php">Delete Item Enchant from Database</a><br />
					<a href="deleteblockdrop.php">Delete Block Drop from Database</a><br />
					<a href="deleteharvesttool.php">Delete Harvest Tool from Database</a><br />
					<a href="deleteitemeffect.php">Delete Item Effect from Database</a><br />
					<a href="deleteblockeffect.php">Delete Block Effect from Database</a><br />
					<a href="deleteentityeffect.php">Delete Entity Effect from Database</a><br />
					<a href="deleteentitydrop.php">Delete Entity Drop from Database</a><br />
					<a href="deleteitementitycanequip.php">Delete Item Entity Can Equip from Database</a><br />
					<a href="deleteitementitybreedswith.php">Delete Item Entity Breeds With from Database</a><br />
				</td>
				<td valign="top">
					<form action="http://localhost/minecraft_interface/files/deletecraftingrecipe.php" method="post">
						<b>Delete Crafting Recipe</b>
						<p>Input ID 1:
							<input type="text" name="cr_iid1" size="30" value="" />
						</p>
						<p>Input ID 2:
							<input type="text" name="cr_iid2" size="30" value="" />
						</p>
						<p>Input ID 3:
							<input type="text" name="cr_iid3" size="30" value="" />
						</p>
						<p>Input ID 4:
							<input type="text" name="cr_iid4" size="30" value="" />
						</p>
						<p>Input ID 5:
							<input type="text" name="cr_iid5" size="30" value="" />
						</p>
						<p>Input ID 6:
							<input type="text" name="cr_iid6" size="30" value="" />
						</p>
						<p>Input ID 7:
							<input type="text" name="cr_iid7" size="30" value="" />
						</p>
						<p>Input ID 8:
							<input type="text" name="cr_iid8" size="30" value="" />
						</p>
						<p>Input ID 9:
							<input type="text" name="cr_iid9" size="30" value="" />
						</p>
						<p>Output ID:
							<input type="text" name="cr_oid" size="30" value="" />
						</p>
						<p>
							<input type="submit" name="submit" value="Delete" />
						</p>
					</form>
					<?php
					if(isset($_POST['submit'])){
						$errors = array();
						if(empty(trim($_POST['cr_iid1']))){
							$id1 = 'Empty';
						} else {
							$id1 = trim($_POST['cr_iid1']);
						}
						if(empty(trim($_POST['cr_iid2']))){
							$id2 = 'Empty';
						} else {
							$id2 = trim($_POST['cr_iid2']);
						}
						if(empty(trim($_POST['cr_iid3']))){
							$id3 = 'Empty';
						} else {
							$id3 = trim($_POST['cr_iid3']);
						}
						if(empty(trim($_POST['cr_iid4']))){
							$id4 = 'Empty';
						} else {
							$id4 = trim($_POST['cr_iid4']);
						}
						if(empty(trim($_POST['cr_iid5']))){
							$id5 = 'Empty';
						} else {
							$id5 = trim($_POST['cr_iid5']);
						}
						if(empty(trim($_POST['cr_iid6']))){
							$id6 = 'Empty';
						} else {
							$id6 = trim($_POST['cr_iid6']);
						}
						if(empty(trim($_POST['cr_iid7']))){
							$id7 = 'Empty';
						} else {
							$id7 = trim($_POST['cr_iid7']);
						}
						if(empty(trim($_POST['cr_iid8']))){
							$id8 = 'Empty';
						} else {
							$id8 = trim($_POST['cr_iid8']);
						}
						if(empty(trim($_POST['cr_iid9']))){
							if($id1 == 'Empty' && $id2 == 'Empty' && $id3 == 'Empty' && $id4 == 'Empty' && $id5 == 'Empty' && $id6 == 'Empty' && $id7 == 'Empty' && $id8 == 'Empty'){
								$errors[] = 'No Recipe Exists with No Input';
							} else {
								$id9 = 'Empty';
							}
						} else {
							$id9 = trim($_POST['cr_iid9']);
						}
						if(empty(trim($_POST['cr_oid']))){
							$errors[] = 'Missing Output ID';
						} else {
							$id10 = trim($_POST['cr_oid']);
						}
						
						if(empty($errors)){
							require_once('../mysqli_connect.php');
							$query = "DELETE FROM crafting_recipe WHERE IID1 = ? AND IID2 = ? AND IID3 = ? AND IID4 = ? AND IID5 = ? AND IID6 = ? AND IID7 = ? AND IID8 = ? AND IID9 = ? AND OID = ?";
							$stmt = mysqli_prepare($dbc, $query);
							
							mysqli_stmt_bind_param($stmt, "ssssssssss", $id1, $id2, $id3, $id4, $id5, $id6, $id7, $id8, $id9, $id10);
							mysqli_stmt_execute($stmt);
							$affected_rows = mysqli_stmt_affected_rows($stmt);
							if($affected_rows == 1) {
								echo 'Crafting Recipe Deleted Successfully';
								mysqli_stmt_close($stmt);
								mysqli_close($dbc);
							} else {
								echo 'ERROR<br />';
								echo mysqli_error($dbc);
								mysqli_stmt_close($stmt);
								mysqli_close($dbc);
							}
						} else {
							echo 'ERROR<br />';
							foreach($errors as $missing) {
								echo "$missing<br />";
							}
						}
					}
					?>
				</td>
			</tr>
		</table>
	</body>
</html>