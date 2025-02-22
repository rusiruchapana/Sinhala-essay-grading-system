namespace SinhalaEssayGrading.Models;

public class SinhalaEssayRequest
{
    public string EssayText { get; set; }
    public int ExpectedWordCount { get; set; }
    public string Topic { get; set; }
}