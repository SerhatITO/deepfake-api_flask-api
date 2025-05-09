using Microsoft.AspNetCore.Mvc;
using System.IO;
using System;
using System.Net.Http.Headers;
using System.Threading.Tasks;

[Route("api/[controller]")]
[ApiController]
public class VideoAnalyzeController : ControllerBase
{
    private readonly IHttpClientFactory _httpClientFactory;

    public VideoAnalyzeController(IHttpClientFactory httpClientFactory)
    {
        _httpClientFactory = httpClientFactory;
    }

    [HttpPost("analyze")]
    public async Task<IActionResult> AnalyzeVideo([FromForm] IFormFile videoFile)
    {
        if (videoFile == null || videoFile.Length == 0)
            return BadRequest("Video dosyası seçilmedi.");

        var client = _httpClientFactory.CreateClient();
        var requestContent = new MultipartFormDataContent();

        using var memoryStream = new MemoryStream();
        await videoFile.CopyToAsync(memoryStream);
        memoryStream.Position = 0;

        var fileContent = new ByteArrayContent(memoryStream.ToArray());
        fileContent.Headers.ContentType = MediaTypeHeaderValue.Parse("video/mp4");
        requestContent.Add(fileContent, "video", videoFile.FileName);

        try
        {
            var response = await client.PostAsync("http://127.0.0.1:5050/analyze", requestContent);
            var responseBody = await response.Content.ReadAsStringAsync();
            return Content(responseBody, "application/json");
        }
        catch (Exception ex)
        {
            return StatusCode(500, $"Flask API isteği başarısız: {ex.Message}");
        }
    }
}
