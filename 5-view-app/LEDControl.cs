using System;
using System.Collections.Generic;
using System.IO.Ports;
using System.Threading;

public class LEDControl
{
    private SerialPort _serialPort;
    private bool _enable;
    private Queue<byte> _cmdQueue = new Queue<byte>();
    private Thread _sendThread;
    private bool _terminated = false;
    private object _lockObject = new object();

    public LEDControl(string portName = "COM7", int baudRate = 9600, int dataBits = 8, int stopBits = 1)
    {
        _enable = true;
        if (_enable)
        {
            try
            {
                _serialPort = new SerialPort
                {
                    PortName = portName,
                    BaudRate = baudRate,
                    DataBits = dataBits,
                    StopBits = (StopBits)stopBits
                };

                // Set the read/write timeouts
                _serialPort.ReadTimeout = 500;
                _serialPort.WriteTimeout = 500;

                _serialPort.Open();
                _sendThread = new Thread(SendProcess);
                _sendThread.Start();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Failed to connect serial port" + ex.Message);
            }
            
        }
    }

    public bool IsEnable()
    {
        return _enable;
    }

    public void SetAllLedOff()
    {
        lock (_lockObject)
        {
            _cmdQueue.Enqueue(0x27);
        }
    }

    public void SetRedLedOn()
    {
        lock (_lockObject)
        {
            _cmdQueue.Enqueue(0x11);
        }
    }

    public void SetGreenLedOn()
    {
        lock (_lockObject)
        {
            _cmdQueue.Enqueue(0x14);
        }
    }

    public void SetYellowLedOn()
    {
        lock (_lockObject)
        {
            _cmdQueue.Enqueue(0x12);
        }
    }

    private void SendProcess()
    {
        while (!_terminated)
        {
            if (_cmdQueue.Count > 0)
            {
                lock (_lockObject)
                {
                    var msg = _cmdQueue.Dequeue();
                    _serialPort.Write(new byte[] { msg }, 0, 1);
                }
            }
            Thread.Sleep(30);
        }
    }

    public void Close()
    {
        _terminated = true;
        _sendThread.Join();
        if (_serialPort != null && _serialPort.IsOpen)
        {
            _serialPort.Close();
        }
    }

    ~LEDControl()
    {
        Close();
    }
}