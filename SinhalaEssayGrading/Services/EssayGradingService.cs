using System.Diagnostics;
using System.Text.Json;
using System.IO;

public class EssayGradingService
{
    private readonly string _pythonPath = "C:\\Users\\umega\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"; 
    private readonly string _scriptPath = "d:\\Sinhala-essay-grading-system\\SinhalaEssayGrading\\PythonScripts\\grade_essay.py"; // Ensure absolute path

    public async Task<Dictionary<string, double>> GradeEssay(string essayText, int expectedWordCount, string topic)
    {
        var inputData = new
        {
            EssayText = essayText,
            ExpectedWordCount = expectedWordCount,
            Topic = topic
        };

        string inputJson = JsonSerializer.Serialize(inputData);

        // Write JSON data to a temporary file
        string tempFilePath = Path.GetTempFileName();
        await File.WriteAllTextAsync(tempFilePath, inputJson);

        var processStartInfo = new ProcessStartInfo
        {
            FileName = _pythonPath,
            Arguments = $"{_scriptPath} \"{tempFilePath}\"",  // Pass file path instead of JSON string
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        using (var process = new Process { StartInfo = processStartInfo })
        {
            process.Start();
            string result = await process.StandardOutput.ReadToEndAsync();
            string errors = await process.StandardError.ReadToEndAsync();

            process.WaitForExit();

            // Cleanup temp file
            File.Delete(tempFilePath);

            if (!string.IsNullOrEmpty(errors))
                throw new Exception($"Python error: {errors}");

            return JsonSerializer.Deserialize<Dictionary<string, double>>(result);
        }
    }
}
