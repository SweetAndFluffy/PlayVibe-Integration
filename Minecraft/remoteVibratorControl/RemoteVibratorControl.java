package remoteVibratorControl;

import cpw.mods.fml.common.Mod;
import cpw.mods.fml.common.Mod.EventHandler;
import cpw.mods.fml.common.event.*;
import cpw.mods.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.common.config.Configuration;
import net.minecraftforge.event.entity.player.PlayerPickupXpEvent;
import scala.Console;

@Mod(modid="RemoteVibratorControlMod", name="RemoteVibratorControlMod", version="0.1", acceptableRemoteVersions = "*")
public class RemoteVibratorControl {
	private VibratorController vibratorController = null;
	private String playerName = "*";
	private String serverURL = "";
	private float xpMultiplier = 10;
	private float xpDecrease = 2;
	private Configuration config;
	
	@EventHandler
	public void preInit(FMLPreInitializationEvent e)
	{
		 vibratorController = new VibratorController();
		 config = new Configuration(e.getSuggestedConfigurationFile());
		 
		 reloadConfig();
		 
		 vibratorController.setURL(serverURL);
		 vibratorController.setPointReductionBySecond(xpDecrease);
	}
	
	public void reloadConfig()
	{
		 config.load();
		 
		 playerName = config.get("General", "PlayerName", "*").getString();
		 serverURL = config.get("General", "ServerURL", "http://192.168.1.133:5000/").getString();
		 xpMultiplier = config.getFloat("XPMultiplier", "General", 10, 0, 100000, "Gained XP are multiplied by this value, before beeing sent to the vibe.");
		 xpDecrease = config.getFloat("XPDecrease", "General", 2, 1, 100, "XP Decrease per second");
		 
		 config.save();
	}

	@EventHandler
	public void init(FMLInitializationEvent e)
	{
		Console.out().println("Vibartor Controller Initiated!");
	}

	@EventHandler
	public void postInit(FMLPostInitializationEvent e)
	{
		MinecraftForge.EVENT_BUS.register(this);
	}
	
	@SubscribeEvent
	public void playerPickedUpXPEvent(PlayerPickupXpEvent e)
	{
		if(playerName.equals("*") || playerName.equals(e.entityPlayer.getCommandSenderName())) {
			vibratorController.pushPoints(e.orb.xpValue * xpMultiplier);
		}
	}
}
