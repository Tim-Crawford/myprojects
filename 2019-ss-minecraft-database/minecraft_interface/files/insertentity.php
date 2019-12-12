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
					<form action="http://localhost/minecraft_interface/files/insertentity.php" method="post">
						<b>Insert Entity</b>
						<p>ID:
							<input type="text" name="e_id" size="30" value="" />
						</p>
						<p>Name:
							<input type="text" name="e_name" size="30" value="" />
						</p>
						<p>Is Living:
							<input type="text" name="e_livflg" size="30" value="" />
						</p>
						<p>Is Mountable:
							<input type="text" name="e_mount" size="30" value="" />
						</p>
						<p>HP:
							<input type="text" name="e_hp" size="30" value="" />
						</p>
						<p>Can be Led:
							<input type="text" name="e_lead" size="30" value="" />
						</p>
						<p>Can Fly:
							<input type="text" name="e_fly" size="30" value="" />
						</p>
						<p>Is Hostile:
							<input type="text" name="e_hstflg" size="30" value="" />
						</p>
						<p>Is Passive:
							<input type="text" name="e_psvflg" size="30" value="" />
						</p>
						<p>Attack Damage:
							<input type="text" name="e_atkdmg" size="30" value="" />
						</p>
						<p>Is Tameable:
							<input type="text" name="e_tame" size="30" value="" />
						</p>
						<p>
							<input type="submit" name="submit" value="Insert" />
						</p>
					</form>
					<?php
					if(isset($_POST['submit'])){
						$errors = array();
						if(empty(trim($_POST['e_id']))){
							$errors[] = 'Missing Entity ID';
						} else {
							$id = trim($_POST['e_id']);
						}
						if(empty(trim($_POST['e_name']))){
							$errors[] = 'Missing Entity Name';
						} else {
							$name = trim($_POST['e_name']);
						}
						if(empty(trim($_POST['e_livflg']))){
							$livflg = '0';
						} else {
							$livflg = trim($_POST['e_livflg']);
							if($livflg != '0' && $livflg != '1'){
								$errors[] = 'Is Living Must be 0/1';
							}
						}
						if($livflg == '0'){
							$hp = NULL;
							$lead = NULL;
							$fly = NULL;
							$hstflg = '0';
							$psvflg = '0';
							$atkdmg = NULL;
							$tame = NULL;
						} else {
							if(empty(trim($_POST['e_hp']))){
								$hp = '1';
							} else {
								$hp = trim($_POST['e_hp']);
								if($hp <= '0'){
									$errors[] = 'HP Must be Greater Than 0';
								}
							}
							if(empty(trim($_POST['e_lead']))){
								$lead = '0';
							} else {
								$lead = trim($_POST['e_lead']);
								if($lead != '0' && $lead != '1'){
									$errors[] = 'Can be Led Must be 0/1';
								}
							}
							if(empty(trim($_POST['e_fly']))){
								$fly = '0';
							} else {
								$fly = trim($_POST['e_fly']);
								if($fly != '0' && $fly != '1'){
									$errors[] = 'Can Fly Must be 0/1';
								}
							}
							if(empty(trim($_POST['e_hstflg']))){
								$hstflg = '0';
							} else {
								$hstflg = trim($_POST['e_hstflg']);
								if($hstflg != '0' && $hstflg != '1'){
									$errors[] = 'Is Hostile Must be 0/1';
								}
							}
							if(empty(trim($_POST['e_psvflg']))){
								$psvflg = '0';
							} else {
								$psvflg = trim($_POST['e_psvflg']);
								if($psvflg != '0' && $psvflg != '1'){
									$errors[] = 'Is Passive Must be 0/1';
								}
							}
							if($hstflg == '0'){
								$atkdmg = NULL;
							} else {
								if(empty(trim($_POST['e_atkdmg']))){
									$atkdmg = '0';
								} else {
									$atkdmg = trim($_POST['e_atkdmg']);
									if($atkdmg < '0'){
										$errors[] = 'Attack Damage Cannot be Negative';
									}
								}
							}
							if($psvflg == '0'){
								$tame = NULL;
							} else {
								if(empty(trim($_POST['e_tame']))){
									$tame = '0';
								} else {
									$tame = trim($_POST['e_tame']);
									if($tame != '0' && $tame != '1'){
										$errors[] = 'Is Tameable Must be 0/1';
									}
								}
							}
						}
						if($livflg == '1' && $psvflg == '0'){
							$mount = NULL;
						} else {
							if(empty($_POST['e_mount'])){
								$mount = '0';
							} else {
								$mount = trim(trim($_POST['e_mount']));
								if($mount != '0' && $mount != '1'){
									$errors[] = 'Is Mountable Must be 0/1';
								}
							}
						}
						
						if(empty($errors)){
							require_once('../mysqli_connect.php');
							$query = "INSERT INTO entity (ID, Name, LivingFlag, Mount, HP, Lead, Fly, HostileFlag, PassiveFlag, AtkDmg, Tame)
										VALUES (?,?,?,?,?,?,?,?,?,?,?)";
							$stmt = mysqli_prepare($dbc, $query);
							
							mysqli_stmt_bind_param($stmt, "ssiiiiiiiii", $id, $name, $livflg, $mount, $hp, $lead, $fly, $hstflg, $psvflg, $atkdmg, $tame);
							mysqli_stmt_execute($stmt);
							$affected_rows = mysqli_stmt_affected_rows($stmt);
							if($affected_rows == 1) {
								echo 'Entity Inserted Successfully';
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