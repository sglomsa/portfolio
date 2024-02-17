using UnityEngine;

public class GameManager : MonoBehaviour {
    
    public int level = 1;
    public int score;
    public int lives = 3;

    private void Awake() {
        DontDestroyOnLoad(this.gameObject);
    }

    private void Start() {
        NewGame();
    }

    private void NewGame() {
        this.score = 0;
        this.lives = 3;
    }
}
