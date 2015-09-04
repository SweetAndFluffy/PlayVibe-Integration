package remoteVibratorControl;

import net.minecraft.command.CommandBase;
import net.minecraft.command.ICommandSender;

public class ReloadVibeConfigCommand extends CommandBase {
	private RemoteVibratorControl remoteVibratorControl = null;
	
	public ReloadVibeConfigCommand(RemoteVibratorControl remoteVibeControl) {
		remoteVibratorControl = remoteVibeControl;
	}
	
	@Override
	public String getCommandName() {
		return "reloadVibeConf";
	}
	@Override
	public String getCommandUsage(ICommandSender p_71518_1_) {
		return "Reloads the vibe config.";
	}
	@Override
	public void processCommand(ICommandSender p_71515_1_, String[] p_71515_2_) {
		remoteVibratorControl.reloadConfig();
	}
}
