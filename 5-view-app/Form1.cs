using System;
using System.Drawing;
using System.IO;
using System.Net.Http;
using System.Threading;
using System.Windows.Forms;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Diagnostics;
using System.Windows.Forms;
using System.Net;
using Microsoft.Web.WebView2.WinForms;
using System.Windows.Forms;
using System.Security.Permissions;
using System.Net.Http.Json;
using System.Text;


namespace KioskHttpClientApp
{
    public partial class Form1 : Form
    {
        private readonly System.Windows.Forms.Timer _timer;
        private readonly HttpClient _httpClient;
        private readonly LEDControl _ledControl;
        private WebView2 _webView;
        private string apiUrl = "http://localhost:8012/api/stream";
        private int requestInterval = 1000;

        private Thread _httpGetThread;
        private bool _continue = true;



        public Form1()
        {
            InitializeComponent();
            InitializeWebView();

            this.tabControl.Selected += new TabControlEventHandler(tabControl_Selected);

            _ledControl = new LEDControl();
            _ledControl.SetAllLedOff();

            _httpClient = new HttpClient();

            _httpGetThread = new Thread(getDetectResult);
            _httpGetThread.Start();

        }
        protected override void OnFormClosing(FormClosingEventArgs e)
        {
            _continue = false;
            if (_httpGetThread != null && _httpGetThread.IsAlive)
            {
                _httpGetThread.Join();
            }

            _timer.Stop();
            _httpClient.Dispose();
            _ledControl.SetAllLedOff();
            _ledControl.Close();
            if (_webView != null)
            {
                pictureBox1.Controls.Remove(_webView);
                _webView.Dispose();
                _webView = null;
            }
            base.OnFormClosing(e);
        }

        private void InitializeWebView()
        {
            _webView = new WebView2
            {
                Dock = DockStyle.Fill,
                Source = new Uri(apiUrl)
            };
            pictureBox1.Controls.Add(_webView);
        }


        private async void getDetectResult()
        {
            while (_continue)
            {
                using (HttpClient httpClient = new HttpClient())
                {
                    string apiUrl = "http://localhost:8012/api/detect";
                    try
                    {
                        HttpResponseMessage response = await httpClient.GetAsync(apiUrl);
                        if (response.IsSuccessStatusCode)
                        {
                            string content = await response.Content.ReadAsStringAsync();

                            ApiResponse apiResponse = JsonSerializer.Deserialize<ApiResponse>(content);

                            if (apiResponse != null)
                            {
                                //MessageBox.Show($"Class Name: {apiResponse.Result.ClassName}\n" +
                                //                $"Class ID: {apiResponse.Result.ClassId}\n" +
                                //                $"Confidence: {apiResponse.Result.ClassConfidence}\n" +
                                //                $"Latency: {apiResponse.Result.LatencyMs} ms\n" +
                                //                $"Timestamp: {apiResponse.Timestamp} \n" +
                                //                $"Alarm: {apiResponse.Alarm}");


                                switch (apiResponse.Alarm)
                                {
                                    case -1:
                                        {
                                            _ledControl.SetAllLedOff();
                                        }
                                        break;
                                    case 0:
                                        {
                                            _ledControl.SetAllLedOff();
                                            _ledControl.SetGreenLedOn();
                                        }
                                        break;
                                    case 1:
                                        {
                                            _ledControl.SetAllLedOff();
                                            _ledControl.SetYellowLedOn();
                                        }
                                        break;
                                    case 2:
                                        {
                                            _ledControl.SetAllLedOff();
                                            _ledControl.SetRedLedOn();
                                        }
                                        break;
                                }


                                //if (apiResponse.Result.ClassId == 6) // Skipping
                                //{
                                //    if (apiResponse.Result.ClassConfidence > 0.7)
                                //    {
                                //        _ledControl.SetAllLedOff();
                                //        _ledControl.SetRedLedOn();

                                //        //MessageBox.Show("Danger: " + apiResponse.Result.ClassName + " (" + apiResponse.Result.ClassConfidence.ToString() + " )");
                                //    }
                                //    else if (apiResponse.Result.ClassConfidence > 0.3)
                                //    {
                                //        _ledControl.SetAllLedOff();
                                //        _ledControl.SetYellowLedOn();
                                //        //MessageBox.Show("Warning: " + apiResponse.Result.ClassName + " (" + apiResponse.Result.ClassConfidence.ToString() + " )");
                                //    }
                                //    else
                                //    {
                                //        _ledControl.SetAllLedOff();
                                //        _ledControl.SetGreenLedOn();
                                //    }
                                //}
                                //else if (apiResponse.Result.ClassId == 7) // Two at a time
                                //{
                                //    if (apiResponse.Result.ClassConfidence > 0.85)
                                //    {
                                //        _ledControl.SetAllLedOff();
                                //        _ledControl.SetRedLedOn();

                                //        //MessageBox.Show("Danger: " + apiResponse.Result.ClassName + " (" + apiResponse.Result.ClassConfidence.ToString() + " )");
                                //    }
                                //    else if (apiResponse.Result.ClassConfidence > 0.6)
                                //    {
                                //        _ledControl.SetAllLedOff();
                                //        _ledControl.SetYellowLedOn();
                                //        //MessageBox.Show("Warning: " + apiResponse.Result.ClassName + " (" + apiResponse.Result.ClassConfidence.ToString() + " )");
                                //    }
                                //    else
                                //    {
                                //        _ledControl.SetAllLedOff();
                                //        _ledControl.SetGreenLedOn();
                                //    }
                                //}
                                //else if (apiResponse.Result.ClassId == 8) // Coverup
                                //{
                                //    if (apiResponse.Result.ClassConfidence > 0.8)
                                //    {
                                //        _ledControl.SetAllLedOff();
                                //        _ledControl.SetRedLedOn();

                                //        //MessageBox.Show("Danger: " + apiResponse.Result.ClassName + " (" + apiResponse.Result.ClassConfidence.ToString() + " )");
                                //    }
                                //    else if (apiResponse.Result.ClassConfidence > 0.4)
                                //    {
                                //        _ledControl.SetAllLedOff();
                                //        _ledControl.SetYellowLedOn();
                                //        //MessageBox.Show("Warning: " + apiResponse.Result.ClassName + " (" + apiResponse.Result.ClassConfidence.ToString() + " )");
                                //    }
                                //    else
                                //    {
                                //        _ledControl.SetAllLedOff();
                                //        _ledControl.SetGreenLedOn();
                                //    }
                                //}
                                //else if (apiResponse.Result.ClassId == 9) // Hide behind
                                //{
                                //    if (apiResponse.Result.ClassConfidence > 0.7)
                                //    {
                                //        _ledControl.SetAllLedOff();
                                //        _ledControl.SetRedLedOn();
                                //        //MessageBox.Show("Danger: " + apiResponse.Result.ClassName + " (" + apiResponse.Result.ClassConfidence.ToString() + " )");
                                //    }
                                //    else if (apiResponse.Result.ClassConfidence > 0.4)
                                //    {
                                //        _ledControl.SetAllLedOff();
                                //        _ledControl.SetYellowLedOn();
                                //        //MessageBox.Show("Warning: " + apiResponse.Result.ClassName + " (" + apiResponse.Result.ClassConfidence.ToString() + " )");
                                //    }
                                //    else
                                //    {
                                //        _ledControl.SetAllLedOff();
                                //        _ledControl.SetGreenLedOn();
                                //    }
                                //}

                                //else if (apiResponse.Result.ClassId == 5 && apiResponse.Result.ClassConfidence > 0.4) // Normal
                                //{
                                //    _ledControl.SetAllLedOff();
                                //    _ledControl.SetGreenLedOn();
                                //    //MessageBox.Show("Normal" + " (" + apiResponse.Result.ClassId.ToString() + " )");
                                //}
                                //else if(apiResponse.Result.ClassId == 0 && apiResponse.Result.ClassConfidence > 0.4)
                                //{
                                //    _ledControl.SetAllLedOff();
                                //}
                                //else
                                //{
                                //    _ledControl.SetAllLedOff();
                                //    _ledControl.SetGreenLedOn();
                                //}

                            }
                            else
                            {
                                MessageBox.Show("Failed to parse JSON.");
                                _ledControl.SetAllLedOff();
                            }
                        }
                        else
                        {
                            MessageBox.Show("Request failed: " + response.StatusCode);
                            _ledControl.SetAllLedOff();
                        }
                    }
                    catch (HttpRequestException ex)
                    {
                        //MessageBox.Show("Exception: " + ex.Message);
                        _ledControl.SetAllLedOff();
                    }
                }

                Thread.Sleep(100);
            }
        }



        private async void btnGet_Click(object sender, EventArgs e)
        {
            //MessageBox.Show("GET");

            using (HttpClient httpClient = new HttpClient())
            {
                string apiUrl = "http://localhost:8012/api/detect";

                try
                {
                    HttpResponseMessage response = await httpClient.GetAsync(apiUrl);
                    if (response.IsSuccessStatusCode)
                    {
                        string content = await response.Content.ReadAsStringAsync();

                        ApiResponse apiResponse = JsonSerializer.Deserialize<ApiResponse>(content);

                        if (apiResponse != null)
                        {
                            MessageBox.Show($"Class Name: {apiResponse.Result.ClassName}\n" +
                                            $"Class ID: {apiResponse.Result.ClassId}\n" +
                                            $"Confidence: {apiResponse.Result.ClassConfidence}\n" +
                                            $"Latency: {apiResponse.Result.LatencyMs} ms\n" +
                                            $"Timestamp: {apiResponse.Timestamp} \n" +
                                            $"Alarm: {apiResponse.Alarm}");

                        }
                        else
                        {
                            MessageBox.Show("Failed to parse JSON.");
                        }
                    }
                    else
                    {
                        MessageBox.Show("Request failed: " + response.StatusCode);
                    }
                }
                catch (HttpRequestException ex)
                {
                    MessageBox.Show("Exception: " + ex.Message);
                }
            }
        }

        private void btnLedTest_Click(object sender, EventArgs e)
        {
            _ledControl.SetAllLedOff();
            _ledControl.SetGreenLedOn();
            Thread.Sleep(500);
            _ledControl.SetAllLedOff();
            _ledControl.SetYellowLedOn();
            Thread.Sleep(500);
            _ledControl.SetAllLedOff();
            _ledControl.SetRedLedOn();
            Thread.Sleep(500);
            _ledControl.SetAllLedOff();

        }

        private async void btnGetDetectRoi_Click(object sender, EventArgs e)
        {
            using (HttpClient httpClient = new HttpClient())
            {
                string apiUrl = "http://localhost:8012/api/detect/getroi";

                try
                {
                    HttpResponseMessage response = await httpClient.GetAsync(apiUrl);
                    if (response.IsSuccessStatusCode)
                    {
                        string content = await response.Content.ReadAsStringAsync();


                        ApiResponseROI apiResponseROI = JsonSerializer.Deserialize<ApiResponseROI>(content);

                        if (apiResponseROI != null)
                        {
                            MessageBox.Show($"x_start: {apiResponseROI.Xstart}\n" +
                                            $"y_start: {apiResponseROI.Ystart}\n" +
                                            $"x_end: {apiResponseROI.Xend}\n" +
                                            $"y_end: {apiResponseROI.Yend}\n");
                        }
                        else
                        {
                            MessageBox.Show("Failed to parse JSON.");
                        }
                    }
                    else
                    {
                        MessageBox.Show("Request failed: " + response.StatusCode);
                    }
                }
                catch (HttpRequestException ex)
                {
                    MessageBox.Show("Exception: " + ex.Message);
                }
            }
        }

        //private async void tabPageSettings_Click(object sender, EventArgs e)
        //{
        //    MessageBox.Show("Capture frame");

        //    if (_webView != null)
        //    {
        //        using (var stream = new MemoryStream())
        //        {
        //            await _webView.CoreWebView2.CapturePreviewAsync(
        //                Microsoft.Web.WebView2.Core.CoreWebView2CapturePreviewImageFormat.Png,
        //                stream);

        //            stream.Position = 0;
        //            Bitmap bitmap = new Bitmap(stream);
        //            pictureBox2.Image = bitmap;
        //        }
        //    }
        //}


        private async void tabControl_Selected(Object sender, TabControlEventArgs e)
        {

            //System.Text.StringBuilder messageBoxCS = new System.Text.StringBuilder();
            //messageBoxCS.AppendFormat("{0} = {1}", "TabPage", e.TabPage);
            //messageBoxCS.AppendLine();
            //messageBoxCS.AppendFormat("{0} = {1}", "TabPageIndex", e.TabPageIndex);
            //messageBoxCS.AppendLine();
            //messageBoxCS.AppendFormat("{0} = {1}", "Action", e.Action);
            //messageBoxCS.AppendLine();
            //MessageBox.Show(messageBoxCS.ToString(), "Selected Event");

            await ResetROI();

            if (_webView != null)
            {
                using (var stream = new MemoryStream())
                {
                    await _webView.CoreWebView2.CapturePreviewAsync(
                        Microsoft.Web.WebView2.Core.CoreWebView2CapturePreviewImageFormat.Png,
                        stream);

                    stream.Position = 0;
                    Bitmap bitmap = new Bitmap(stream);
                    pictureBox2.Image = bitmap;
                }
            }
        }


        private async void button3_Click(object sender, EventArgs e)
        {
            var roiData = new
            {
                x_start = 100,
                y_start = 200,
                x_end = 300,
                y_end = 400
            };

            string json = JsonSerializer.Serialize(roiData);

            string url = "http://localhost:8012/api/detect/setroi";

            using (HttpClient client = new HttpClient())
            {
                var content = new StringContent(json, Encoding.UTF8, "application/json");
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    MessageBox.Show("ROI 設置成功");
                }
                else
                {
                    MessageBox.Show("ROI 設置失敗: " + response.StatusCode);
                }
            }
        }

        private async void btnApply_Click(object sender, EventArgs e)
        {
            int current_x_start = ((int)numericUpDownXstart.Value);
            int current_y_start = ((int)numericUpDownYstart.Value);
            int current_x_end = ((int)numericUpDownXend.Value);
            int current_y_end = ((int)numericUpDownYend.Value);

            var roiData = new
            {
                x_start = current_x_start,
                y_start = current_y_start,
                x_end = current_x_end,
                y_end = current_y_end
            };

            string json = JsonSerializer.Serialize(roiData);
            string url = "http://localhost:8012/api/detect/setroi";

            using (HttpClient client = new HttpClient())
            {
                var content = new StringContent(json, Encoding.UTF8, "application/json");
                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    MessageBox.Show("ROI Updated Successfully");
                }
                else
                {
                    MessageBox.Show("ROI Updated Failed: " + response.StatusCode);
                }
            }

        }

        private async void btnReset_Click(object sender, EventArgs e)
        {
            await ResetROI();
        }
        private async Task ResetROI()
        {
            using (HttpClient httpClient = new HttpClient())
            {
                string apiUrl = "http://localhost:8012/api/detect/getroi";
                try
                {
                    HttpResponseMessage response = await httpClient.GetAsync(apiUrl);
                    if (response.IsSuccessStatusCode)
                    {
                        string content = await response.Content.ReadAsStringAsync();
                        ApiResponseROI apiResponseROI = JsonSerializer.Deserialize<ApiResponseROI>(content);

                        if (apiResponseROI != null)
                        {
                            //MessageBox.Show($"x_start: {apiResponseROI.Xstart}\n" +
                            //                $"y_start: {apiResponseROI.Ystart}\n" +
                            //                $"x_end: {apiResponseROI.Xend}\n" +
                            //                $"y_end: {apiResponseROI.Yend}\n");

                            numericUpDownXstart.Value = (int)apiResponseROI.Xstart;
                            numericUpDownYstart.Value = (int)apiResponseROI.Ystart;
                            numericUpDownXend.Value = (int)apiResponseROI.Xend;
                            numericUpDownYend.Value = (int)apiResponseROI.Yend;
                        }
                        else
                        {
                            MessageBox.Show("Failed to parse JSON.");
                        }
                    }
                    else
                    {
                        MessageBox.Show("Request failed: " + response.StatusCode);
                    }
                }
                catch (HttpRequestException ex)
                {
                    MessageBox.Show("Exception: " + ex.Message);
                }
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }


    public class Result
    {
        [JsonPropertyName("class_name")]
        public string ClassName { get; set; }

        [JsonPropertyName("class_id")]
        public int ClassId { get; set; }

        [JsonPropertyName("class_confidence")]
        public float ClassConfidence { get; set; }

        [JsonPropertyName("latency_ms")]
        public int LatencyMs { get; set; }
    }

    public class ApiResponse
    {
        [JsonPropertyName("result")]
        public Result Result { get; set; }

        [JsonPropertyName("timestamp")]
        public string Timestamp { get; set; }

        [JsonPropertyName("status")]
        public int Status { get; set; }
        [JsonPropertyName("alarm")]
        public int Alarm { get; set; }
    }

    public class ApiResponseROI
    {
        [JsonPropertyName("x_start")]
        public double Xstart { get; set; }

        [JsonPropertyName("y_start")]
        public double Ystart { get; set; }

        [JsonPropertyName("x_end")]
        public double Xend { get; set; }

        [JsonPropertyName("y_end")]
        public double Yend { get; set; }
    }

}
