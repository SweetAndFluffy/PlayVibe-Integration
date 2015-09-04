package remoteVibratorControl;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class VibratorController {
	private String url = ""; 
	private ExecutorService executor = null; 
	private float points = 0;
	private float pointsReductionBySecond = 2;
	
	public VibratorController() {
		executor = Executors.newFixedThreadPool(1);
		
		Timer timer = new Timer();
		timer.scheduleAtFixedRate(new TimerTask() {
			@Override
			public void run() {
				if(points - pointsReductionBySecond <= 0) {
					points = 0;
					setRate(points);
				} else {
					points -= pointsReductionBySecond;
					setRate(points);
				}
			}
		}, 1000, 1000);
	}
	public void setURL(String url) {
		this.url = url;
	}
	public void setPointReductionBySecond(float value) {
		pointsReductionBySecond = value;
	}
	public void close() {
		executor.shutdown();
	}
	private static float rateBefore;
	public void setRate(float points) {
		if(points == rateBefore) {
			return;
		}
		rateBefore = points;
		
		if(points > 100) {
			points = 100;
		} else if(points < 0) {
			points = 0;
		}
		
		try {
			executor.submit(new Request(new URL(url + "rate/" + (int) points + "/")));
			System.out.println("Current Value: " + points);
		} catch(MalformedURLException e) {
			
		}
	}
	public void pushPoints(float f) {
		this.points += f;
		this.setRate(this.points);
	}
	public void dropPoints(int amount) {
		this.points -= amount;
		this.setRate(this.points);
	}
}
